import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


args = {
    'owner': 'etl',
    'email': ['etl@yandex.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
}

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
    end = EmptyOperator(task_id='end')

    t_export_from_source_film_work = BashOperator(
        task_id='export_from_source_film_work',
        cwd='/opt/airflow/src',
        bash_command="PYTHONPATH=/home/airflow/venv/lib/python:/opt/airflow/src python /opt/airflow/src/bin/extractors/run_extractor_film_work.py",
        dag=dag
    )

    start >> t_export_from_source_film_work >> end
