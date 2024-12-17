from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
import pendulum
from datetime import timedelta
from airflow.utils.state import State 

with DAG(
    dag_id='dags_external_task_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='0 7 * * *',
    catchup=False
) as dag:
    external_task_sensor_a = ExternalTaskSensor(
        task_id = 'external_task_sensor_a',
        external_dag_id = 'dags_branch_python_operator',
        external_task_id = 'task_a',
        allowed_states = [State.SKIPPED], # 센서가 Success 되기 위한 센싱 대상의 상태
        execution_delta = timedelta(hours=6), # 본 DAG 보다 센싱할 DAG이 얼마나 과거에 있나? 현재 기준으로는 센싱할 DAG(dags_branch_python_operator)이 6시간 앞서 있음
        poke_interval=10        #10초
    )

    external_task_sensor_b = ExternalTaskSensor(
        task_id='external_task_sensor_b',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_b',
        failed_states=[State.SKIPPED], # 센서가 FAIL 되기 위한 센싱 대상의 상태
        execution_delta=timedelta(hours=6),
        poke_interval=10        #10초
    )

    external_task_sensor_c = ExternalTaskSensor(
        task_id='external_task_sensor_c',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_c',
        allowed_states=[State.SUCCESS],
        execution_delta=timedelta(hours=6),
        poke_interval=10        #10초
    )