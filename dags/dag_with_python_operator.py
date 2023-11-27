from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args={
    'owner':'harsha',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    Last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"hello world, my name is {first_name} {Last_name} and im {age} years old")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Man')
    
def get_age(ti):
    ti.xcom_push(key='age', value=23)

with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v01',
    description='first dag with python operator',
    start_date=datetime(2023, 11, 23),
    schedule_interval='@daily'

) as dag:
    task1=PythonOperator(
        task_id='greet',
        python_callable=greet,
        # op_kwargs={ 'age': 23}
    )
    task2=PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task3=PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )


    [task3, task2]>>task1