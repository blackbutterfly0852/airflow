import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from airflow.exceptions import AirflowException

with DAG(
    dag_id="dags_python_with_trigger_rule_eg1", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 12, 11, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)

)  as dag:
    bash_upstream_1 = BashOperator(
        task_id = 'bash_upstream_1',
        bash_command = 'echo upstream1'

    ) 
    @task(task_id = 'python_upstream_1')
    def python_upstream_1():
        raise AirflowException('downstream1_1 Exception1')

    @task(task_id = 'python_upstream_2')
    def python_upstream_2():
        print('정상처리')

    @task(task_id = 'python_downdstream_1', trigger_rule='all_done') # 상위 Task 가 모두 수행되면 실행 (실패도 수행된것에 포함)
    def python_downstream_1():
        print('정상처리')

    [bash_upstream_1, python_upstream_1(),python_upstream_2()] >> python_downstream_1()