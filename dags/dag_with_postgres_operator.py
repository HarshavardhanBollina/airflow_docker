from datetime import datetime, timedelta
from airflow import DAG
import csv
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def load_csv_to_postgres():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    with open('/opt/airflow/Airflow_Docker/sample_data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        for row in reader:
            # Assuming the CSV has two columns corresponding to dt and dag_id
            sql = "INSERT INTO dag_runs (dt, dag_id) VALUES (%s, %s)"
            postgres_hook.run(sql, parameters=row)


default_args = {
    'owner':'harsha',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_operator',
    default_args=default_args,
    start_date=datetime(2023, 11, 23),
    schedule_interval='0 0 * * *'
) as dag:

    task1=PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql ="""
            CREATE TABLE IF NOT EXISTS dag_runs (
            dt date ,
            dag_id character varying,
            primary key (dt, dag_id))
           
            """
    )
    task2=PythonOperator(
        task_id='loading_data_from_csv_to_postgrestable',
        python_callable=load_csv_to_postgres
    )

# two tasks

    task1>>task2