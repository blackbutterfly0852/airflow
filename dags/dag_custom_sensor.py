from sensors.seoul_api_data_sensor import SeoulApiDataSensor
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_custom_sensor',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    
    tb_public_wifi_info_1 = SeoulApiDataSensor(
        task_id='tb_public_wifi_info_1',
        dataset_nm='TbPublicWifiInfo',
        base_dt_col='WORK_DTTM',
        day_off=0,
        poke_interval=600,
        mode='reschedule'
    )
    
    tb_public_wifi_info_2 = SeoulApiDataSensor(
        task_id='tb_public_wifi_info_2',
        dataset_nm='TbPublicWifiInfo',
        base_dt_col='WORK_DTTM',
        day_off=-1,
        poke_interval=600,
        mode='reschedule'
    )