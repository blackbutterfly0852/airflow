import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.email import EmailOperator
from airflow.decorators import task


with DAG(
    dag_id="dags_python_email_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 10, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
) as dag:
    @task(task_id = 'someting_task')
    def some_logic(**kwargs):
        from random import choice
        return choice(['Success','Fail'])

    send_email = EmailOperator(
        task_id = 'send_email',
        to = 'kkdw91@naver.com',
        subject = '{{ data_interval_end.in_timezone("Asia/Seoul") | ds }} some_logic 처리결과',
        html_content = ' {{ data_interval_end.in_timezone("Asia/Seoul") | ds}} 처리결과는 <br> \
                        {{ ti.xcom_pull(task_ids = "someting_task") }} 했습니다 <br> '
    )

    some_logic() >> send_email


