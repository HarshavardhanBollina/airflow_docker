from airflow.decorators import dag
from airflow.decorators import task
from datetime import datetime, timedelta


default_args = {
    'owner':'Harsha',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='our_dag_with_python_operator_v01',
     default_args=default_args,
     start_date=datetime(2023, 11, 23),
    schedule_interval='@daily')
def hello_world_etl():
    
    @task
    def get_name():
        return "Jerry"
    @task
    def get_age():
        return 23
    @task
    def greet(name,age):
        print(f"hello worls my name is {name} and i am {age} years old")


    name=get_name()
    age=get_age()
    greet(name=name, age=age)

greet_dag=hello_world_etl()

    
