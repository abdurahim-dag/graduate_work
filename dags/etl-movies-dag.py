import pendulum

from airflow import DAG
from airflow.models.variable import Variable
from airflow.models.connection import Connection
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


args = {
    'owner': 'etl',
    'email': ['etl@yandex.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
}

conn = Connection.get_connection_from_secrets('movies')
movies_server = conn.host
movies_port = conn.port
movies_db = conn.schema
movies_username = conn.login
movies_password = conn.password

conn = Connection.get_connection_from_secrets('staging')
staging_server = conn.host
staging_port = conn.port
staging_db = conn.schema
staging_username = conn.login
staging_password = conn.password

batch_size = Variable.get('batch_size')
dir_path = Variable.get('data_dir')

state = Connection.get_connection_from_secrets('state')
state_host = state.host
state_port = state.port


with DAG(
        'etl-to-staging-dag',
        catchup=False,
        default_args=args,
        description='Dag for load data from source to staging',
        is_paused_upon_creation=True,
        start_date=pendulum.datetime(2023, 9, 1, tz="UTC"),
        schedule_interval='0 0 * * *',  # Задаем расписание выполнения дага.
        tags=['staging', ],
) as dag:
    start = EmptyOperator(task_id='start')
    point1 = EmptyOperator(task_id='point-1')
    point2 = EmptyOperator(task_id='point-2')
    end = EmptyOperator(task_id='end')

    groups_export = []
    for script in ['run_extractor_film_work', 'run_extractor_genre', 'run_extractor_person', 'run_extractor_genre_film_work', 'run_extractor_person_film_work']:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/extractors/{{params.script}}.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}' '{{params.state_host}}' '{{params.state_port}}'",
            params = {
                'script': script,
                'host': movies_server,
                'port': movies_port,
                'db': movies_db,
                'username': movies_username,
                'password': movies_password,
                'batch_size': batch_size,
                'dir_path': dir_path,
                'state_host': state_host,
                'state_port': state_port
            },
            dag=dag
        )
        groups_export.append(task)

    groups_transform = []
    for script in ['run_transformer_film_work', 'run_transformer_genre', 'run_transformer_genre_film_work', 'run_transformer_person', 'run_transformer_person_film_work']:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/transformers/{{params.script}}.py '{{params.dir_path}}'",
            params = {
                'script': script,
                'dir_path': dir_path,
            },
            dag=dag
        )
        groups_transform.append(task)

    groups_load = []
    for script in ['run_loader_film_work', 'run_loader_genre', 'run_loader_genre_film_work', 'run_loader_person', 'run_loader_person_film_work']:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/loaders/{{params.script}}.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}'",
            params = {
                'script': script,
                'host': staging_server,
                'port': staging_port,
                'db': staging_db,
                'username': staging_username,
                'password': staging_password,
                'batch_size': batch_size,
                'dir_path': dir_path,
            },
            dag=dag
        )

        groups_load.append(task)


    start >> groups_export >> point1 >> groups_transform >> point2 >> groups_load >> end
