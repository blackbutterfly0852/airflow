import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.email import EmailOperator


with DAG(
    dag_id="dags_email_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 8 1 * *",
    start_date=pendulum.datetime(2024, 11, 29, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    # [START howto_operator_bash]
    send_email_task = EmailOperator( # 오퍼레이터가 테스크를 생성
        task_id="send_email_task", # 테스크명과 일치
        to='kkdw91@naver.com',
        cc='kkkdw91@naver.com',
        subject="Airflow 성공메일",
        html_content='Airflow 작업 성공'
    )

    

    