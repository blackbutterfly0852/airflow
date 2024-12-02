import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from common.common_func import regist
from airflow.decorators import task

with DAG(
    dag_id="dags_python_with_op_args", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 3, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    @task(task_id = "regist_t2")
    def regist_f2(name, sex, *args):
        print(f'이름_2 : {name}')
        print(f'성별_2 : {sex}')
        print(f'기타옵션들_2 : {args}')

    
    regist_t1 = PythonOperator(
        task_id = 'regist_t1',
        python_callable=regist,
        op_args=['kim','man','kr','seoul']
    )
    regist_t1
    regist_t2 = regist_f2('nam','women','kr','seoul','jekidong')