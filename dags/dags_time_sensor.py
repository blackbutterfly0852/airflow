import pendulum
from airflow import DAG
from airflow.sensors.date_time import DateTimeSensor

with DAG(
    dag_id="dags_time_sensor",
    start_date=pendulum.datetime(2024, 12, 26, 0, 0, 0),
    end_date=pendulum.datetime(2023, 12, 26, 1, 0, 0),
    schedule="*/10 * * * *",
    catchup=True,
) as dag:
    
    sync_sensor = DateTimeSensor(
        task_id = 'sync_sensor',
        target_time="""{{ macros.datetime.utcnow() + macros.timedelta(minutes=5)}} """ # 현재시간보다 5분 뒤 시작, 슬롯차지

    )