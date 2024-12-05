import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
import random

with DAG(
    dag_id="dags_python_templates", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2024, 11, 29, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    def python_funcion1(start_date, end_date, **kwargs):
        print('### python_function1_start')
        print('start_date : ' + start_date)
        print('end_date : ' + end_date)
        print('### python_function1_end')

    python_t1 = PythonOperator(
        task_id = 'python_t1',
        python_callable=python_funcion1,
        op_kwargs={
            'start_date' : '{{ data_interval_start  | ds}}',
            'end_date' : '{{ data_interval_end | ds}}'
        }
    )

    @task(task_id = 'python_t2')
    def python_funcion2(**kwargs):
        print('### python_function2_start')

        print(kwargs)
        print('ds : ' + kwargs['ds'])
        print('ts : ' + kwargs['ts'])
        print('data_interval_start : ' + str(kwargs['data_interval_start']))
        print('data_interval_end : ' + str(kwargs['data_interval_end']))
        print('task_instance : ' + str(kwargs['task_instance']))
        
        print('### python_function2_end')

    python_t1 >> python_funcion2()