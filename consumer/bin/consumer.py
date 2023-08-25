import time
import uuid
from collections import defaultdict
from contextlib import contextmanager
from typing import Generator

import clickhouse_connect
import confluent_kafka
import pendulum
import psycopg
import pydantic
import storage
from utils import json_decoder, logger, on_exception

from core import Settings
from models import Message


class Executer:
    """Управление процессом ETL из Kafka в Clickhouse."""

    def __init__(
        self, settings: Settings,
        offset_storage: storage.state.BaseOffsetStorage,
        model: pydantic.BaseModel,
    ):
        self._settings = settings
        self._model = model
        self._data_filename = 'data.csv'
        self._column_names = tuple(model.__fields__.keys())
        self._offset_storage = offset_storage
        # Словарь будет хранить офсеты прочитанных партиций
        self._partitions: dict[int, int] = defaultdict(int)

    def _assign(
        self,
        consumer: confluent_kafka.Consumer,
        partitions: list[confluent_kafka.TopicPartition],
    ):
        """Callback на изменения назначений партиций."""
        for partition in partitions:
            logger.info(f"Assign partition: {partition.partition}")
            partition.offset = self._offset_storage.retrieve(partition.partition)

        consumer.assign(partitions)

    @contextmanager
    def _get_consumer(self) -> Generator[confluent_kafka.Consumer, None, None]:
        """Инициализация и возврат консьюмера."""
        consumer = confluent_kafka.Consumer(
            {
                'bootstrap.servers': self._settings.kafka_server,
                'group.id': self._settings.group_id,
                'auto.offset.reset': 'error',
                'partition.assignment.strategy': 'roundrobin',
                'enable.auto.commit': 'false',
                'session.timeout.ms': '45000',
                'broker.address.family': 'v4',
            }
        )
        consumer.subscribe([self._settings.topic], on_assign=self._assign)
        try:
            yield consumer
        finally:
            consumer.close()


    @on_exception(exception=psycopg.errors.DatabaseError, logger=logger)
    @contextmanager
    def _get_cursor(self) -> Generator[psycopg.cursor.Cursor, None, None]:
        """Получение курсора PG."""
        with psycopg.connect(
            host=self._settings.pg_host,
            port=self._settings.pg_port,
            user=self._settings.pg_username,
            password=self._settings.pg_password,
            dbname=self._settings.pg_db,
        ) as conn:
            yield conn.cursor()

    def _to_deadletter_queue(self, message: bytes):
        logger.error('Exception on message to model: %s', (str(message),))

    def _to_csv_line(self, model: Message):
        # Приведём формат времени к clickhouse
        model.timestamp = model.timestamp.format('YYYY-MM-DD hh:mm:ss')
        return (
            ','.join([str(getattr(model, field, '')) for field in self._column_names])
            + '\n'
        )

    def _messages_to_csv(self, messages: list[confluent_kafka.Message]):
        """Сохранение и проверка сообщений."""
        with open(self._data_filename, 'wt') as csv:
            for message in messages:
                try:
                    msg = json_decoder(message.value())
                    # Transform.
                    model = Message(
                        id=int(msg['id']),
                        user_id=uuid.UUID(msg['user_id']),
                        film_id=uuid.UUID(msg['film_id']),
                        frameno=int(msg['frameno']),
                        timestamp=pendulum.parse(msg['timestamp']),
                    )
                    csv.write(self._to_csv_line(model))
                except Exception as e:
                    # Все неправильные сообщения обрабатываем отдельно
                    self._to_deadletter_queue(message.value())
                    logger.error(e)

    def _save_offsets(self):
        """Сохранение офсетов партиций."""
        for partition, offset in self._partitions.items():
            self._offset_storage.save(partition, offset)

    def _process_messages(self, messages: list[confluent_kafka.Message]):
        """Отправка сообщений в clickhouse и сохранение офсетов."""
        if messages:
            self._messages_to_csv(messages)
            self._data_to_db()
            self._save_offsets()

    @on_exception(exception=psycopg.errors.DatabaseError, logger=logger)
    def _data_to_db(self):
        """Сохраняем сообщения в слой."""
        insert_file(
            self.client,
            self._settings.ch_table,
            self._data_filename,
            column_names=self._column_names,
            database=self._settings.ch_db,
        )

    def _no_error(self, msg: confluent_kafka.Message):
        """Сообщаем об отсутствии ошибок при чтении сообщения."""
        err = msg.error()
        if err:
            if err.code() != confluent_kafka.KafkaError._PARTITION_EOF:
                raise confluent_kafka.KafkaException(msg.error())
        return True

    def run(self):
        """Запуск цикла процесса ETL."""
        consumer: confluent_kafka.Consumer
        msg: confluent_kafka.Message
        messages: list[confluent_kafka.Message] = []
        timeout_seconds = self._settings.batch_timeout

        with self._get_consumer() as consumer:
            with self._get_client_db():
                while True:
                    # Extract.
                    msg = consumer.poll(1.0)

                    # Ограничиваем процесс по времени
                    if msg is None:
                        timeout_seconds -= 1
                        if timeout_seconds >= 0:
                            continue

                    # Проверяем на ошибки
                    if msg and self._no_error(msg):
                        messages.append(msg)
                        self._partitions[msg.partition()] = msg.offset() + 1

                    messages_read = len(messages)
                    if (
                        timeout_seconds > 0
                        and messages_read < self._settings.batch_size
                    ):
                        continue

                    # Load.
                    self._process_messages(messages)

                    # Сбрасываем
                    messages = []
                    timeout_seconds = self._settings.batch_timeout
                    self._partitions = defaultdict(int)

                    if messages_read:
                        logger.warning(f"Pushed {messages_read} messages")
                    else:
                        logger.warning('No messages, to sleep')
                        time.sleep(5)


if __name__ == '__main__':
    settings = Settings()
    executer = Executer(
        settings=settings,
        offset_storage=storage.state.RedisOffsetStorage(
            settings.redis_key_prefix, settings.redis_host, settings.redis_port
        ),
    )
    executer.run()
