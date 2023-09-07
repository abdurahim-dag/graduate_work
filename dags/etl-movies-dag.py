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
movies_host = conn.host
movies_port = conn.port
movies_db = conn.schema
movies_username = conn.login
movies_password = conn.password

conn = Connection.get_connection_from_secrets('ods')
ods_host = conn.host
ods_port = conn.port
ods_db = conn.schema
ods_username = conn.login
ods_password = conn.password

conn = Connection.get_connection_from_secrets('elasticsearch')
es_host = conn.host
es_port = conn.port

batch_size = Variable.get('batch_size')
dir_path = Variable.get('data_dir')

state = Connection.get_connection_from_secrets('state')
state_host = state.host
state_port = state.port


with DAG(
        'etl-to-ods-dag',
        catchup=False,
        default_args=args,
        description='Dag for load data from source to ods',
        is_paused_upon_creation=True,
        start_date=pendulum.datetime(2023, 9, 1, tz="UTC"),
        schedule_interval='0 0 * * *',  # Задаем расписание выполнения дага.
        tags=['ods', ],
) as dag:
    start = EmptyOperator(task_id='start')
    point1 = EmptyOperator(task_id='point-1')
    point2 = EmptyOperator(task_id='point-2')
    end = EmptyOperator(task_id='end')

    groups_extract = []
    for script in ['run_extractor_film_work', 'run_extractor_genre', 'run_extractor_person', 'run_extractor_genre_film_work', 'run_extractor_person_film_work']:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/extractors/{{params.script}}.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}' '{{params.state_host}}' '{{params.state_port}}'",
            params = {
                'script': script,
                'host': movies_host,
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
        groups_extract.append(task)

    groups_load_0 = []
    for script in ['run_loader_film_work', 'run_loader_genre', 'run_loader_person',]:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/loaders/{{params.script}}.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}'",
            params = {
                'script': script,
                'host': ods_host,
                'port': ods_port,
                'db': ods_db,
                'username': ods_username,
                'password': ods_password,
                'batch_size': batch_size,
                'dir_path': dir_path,
            },
            dag=dag
        )

        groups_load_0.append(task)

    groups_load_1 = []
    for script in ['run_loader_genre_film_work', 'run_loader_person_film_work']:
        task = BashOperator(
            task_id=script,
            cwd='/opt/airflow/src',
            bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/loaders/{{params.script}}.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}'",
            params = {
                'script': script,
                'host': ods_host,
                'port': ods_port,
                'db': ods_db,
                'username': ods_username,
                'password': ods_password,
                'batch_size': batch_size,
                'dir_path': dir_path,
            },
            dag=dag
        )

        groups_load_1.append(task)

    t_export_views = BashOperator(
        task_id='export_views',
        cwd='/opt/airflow/src',
        bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/extractors/run_extractor_views.py '{{params.host}}' '{{params.port}}' '{{params.db}}' '{{params.username}}' '{{params.password}}' '{{params.batch_size}}' '{{params.dir_path}}' '{{params.state_host}}' '{{params.state_port}}'",
        params = {
            'host': ods_host,
            'port': ods_port,
            'db': ods_db,
            'username': ods_username,
            'password': ods_password,
            'batch_size': batch_size,
            'dir_path': dir_path,
            'state_host': state_host,
            'state_port': state_port
        },
        dag=dag
    )

    t_transform = BashOperator(
        task_id='transform',
        cwd='/opt/airflow/src',
        bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/transformers/run_transform_es.py '{{params.dir_path}}'",
        params = {
            'dir_path': dir_path,
        },
        dag=dag
    )

    t_upload_to_es = BashOperator(
        task_id='upload_to_es',
        cwd='/opt/airflow/src',
        bash_command="source /opt/airflow/venv/bin/activate && PYTHONPATH=/opt/airflow/src python /opt/airflow/src/bin/loaders/run_loader_es_movies.py '{{params.host}}' '{{params.port}}' '{{params.dir_path}}'",
        params = {
            'host': es_host,
            'port': es_port,
            'dir_path': dir_path,
        },
        dag=dag
    )

    start >> groups_extract >> point1 >> groups_load_0 >> point2 >> groups_load_1 >> t_export_views >> t_transform >> t_upload_to_es >> end
