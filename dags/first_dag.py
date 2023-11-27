from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args={

    'owner':"Harsha",
    "retries": 2,
    "retry_delay":timedelta(minutes=2)

}

with DAG(
    dag_id='our_first_dagv2',
    default_args=default_args,
    description='this is the first dag',
    start_date=datetime(2023, 11, 22, 18),
    schedule_interval="@daily"
) as dag:
    task1=BashOperator(
        task_id='first_task',
        bash_command="echo hello worls, this is the first task"

    )

    task2=BashOperator(
        task_id='second_task',
        bash_command='im the second task, i will be running after the succesfull completion of task 1'


    )

    task1>>task2