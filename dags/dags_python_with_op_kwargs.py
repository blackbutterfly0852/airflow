import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from common.common_func import regist2


with DAG(
    dag_id="dags_python_with_op_kwargs", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 3, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    regist2_t1 = PythonOperator(
        task_id = 'regist2_t1',
        python_callable=regist2,
        op_args=['kim','man','kr','seoul'],
        op_kwargs={'email':'kkdw91@naver.com','phone':'010'}
    )
    regist2_t1
    