
import pendulum
from airflow.models.dag import DAG
from airflow.decorators import task


with DAG(
    dag_id="dags_python_show_templates", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 1, tz="Asia/Seoul"),
    catchup=True
) as dag:
    
    @task(task_id = 'python_task')
    def show_templates(**kwargs):
        from pprint import pprint
        pprint(**kwargs)


    show_templates()