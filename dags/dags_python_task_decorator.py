from airflow import DAG
import pendulum
from airflow.decorators import TaskDecorator

with DAG(
    dag_id="dags_python_task_decorator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 2 * * 1",
    start_date=pendulum.datetime(2024, 12, 2, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    
    @task(task_id = "python_task_1")
    def print_conetxt(some_input):
        print(some_input)
    
    python_task_1 = print_conetxt("task_decorator 실행") # python_task_1를 밑에 기재를 안해도 수행