import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import random

with DAG(
    dag_id="dags_python_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2024, 11, 29, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    def select_fruit():
        fruit = ['APPLE', 'BANANA', 'ORANGE', 'AVOCADO']
        rand_int = random.randint(0,3)
        print(fruit[rand_int])

    py_t1 = PythonOperator(
        task_id = 'py_t1',
        python_callable=select_fruit
    )

    py_t1