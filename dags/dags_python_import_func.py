import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
# from plugins.common.common_func import get_sftp > 에어플로우는 에러
from common.common_func import get_sftp


with DAG(
    dag_id="dags_python_import_func", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 11, 29, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    task_get_sftp = PythonOperator(
        task_id = 'task_get_sftp',
        python_callable=get_sftp
    )