from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
import pendulum
from datetime import timedelta
from airflow.utils.state import State 

with DAG(
    dag_id='dags_external_task_sensor',
    start_date=pendulum.datetime(2024,12,17, tz='Asia/Seoul'),
    schedule='0 7 * * *',
    catchup=True
) as dag:
    def calculate_execution_date(execution_date):
    # execution_date에서 6시간 전 시점 계산
        print(f"Current execution_date_1: {execution_date}")
        print(f"Current execution_date_2: {execution_date.in_timezone('Asia/Seoul')}")
        print(f"Current execution_date_3: {execution_date.in_timezone('Asia/Seoul') - timedelta(hours=6)}")
        return execution_date
    
    external_task_sensor_a = ExternalTaskSensor(
        task_id='external_task_sensor_a',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_a',
        allowed_states=[State.SUCCESS], # 센서가 Success 되기 위한 센싱 대상의 상태, # 만족이 안되면 계속 수행
        # 본 DAG 보다 센싱할 DAG이 얼마나 과거에 있나? 현재 기준으로는 센싱할 DAG(dags_branch_python_operator)이 6시간 앞서 있음
        # 만약에 협업환경에서 센싱대상 DAG의 수행시간이나 DAG_ID가 변경할 경우 센싱 대상을 바라보고 있는 센서들의 영향도를 필히 확인 필요
        # execution_delta가 변경되면 센싱대상 DAG을 찾을 수 없음
        execution_delta=timedelta(hours=6),
        #execution_date_fn=calculate_execution_date, 
        poke_interval=10        #10초
    )

    external_task_sensor_b = ExternalTaskSensor(
        task_id='external_task_sensor_b',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_b',
        #failed_states=[State.SKIPPED], # 센서가 FAIL 되기 위한 센싱 대상의 상태
        allowed_states=[State.SKIPPED], # 센서가 FAIL 되기 위한 센싱 대상의 상태
        execution_delta=timedelta(hours=6),
        #execution_date_fn=calculate_execution_date, 
        poke_interval=10        #10초
    )

    external_task_sensor_c = ExternalTaskSensor(
        task_id='external_task_sensor_c',
        external_dag_id='dags_branch_python_operator',
        external_task_id='task_c',
        allowed_states=[State.SKIPPED],
        execution_delta=timedelta(hours=6),
        #execution_date_fn=calculate_execution_date, 
        poke_interval=10        #10초
    )