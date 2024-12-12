import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


with DAG(
    dag_id="dags_trigger_dag_run_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2024, 12, 12, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    
    start_task = BashOperator (
        task_id = 'start_task',
        bash_command = 'echo "start!"'
    )

    trigger_dag_task = TriggerDagRunOperator(
        task_id = 'trigger_dag_task',
        trigger_dag_id='dags_python_operator', # 필수값, 후행 Dag
        trigger_run_id = None, # run_id : 수행방식과 시간을 유일하게 식별 > scheduled_{{ data_interval_start}}, manual_{{execution_date}}, backfill_시간
        execution_date ='{{ data_interval_start }}', # 값이 있으면 트리거가 된 Dag은 manual 수행으로 간주 > manual_{{execution_date}}
        reset_dag_run = True, # True : 이미 수행 이력이 있지만 재수행
        wait_for_completion = False, # t1 > t2 > t3 : t2는 다른 Dag B 수행, B와 t3 간에도 의존관계를 설정하고 싶다면 True로 설정 > t2 & B가 모두 성공일 때 t3 수행
        poke_interval = 60, # Dag B가 성공여부 모니터링 주기
        allowed_states = ['success'], # t2가 성공으로 간주되려면, Dag B는 어떤 상태여야 되는가? 기본은 success이지만 fail도 추가할 수 있음
        failed_states = None # allowd_states와 반대, t2가 실패로 간주되려면, Dag B는 어떤 상태여야 되는가?
    )

    start_task >> trigger_dag_task