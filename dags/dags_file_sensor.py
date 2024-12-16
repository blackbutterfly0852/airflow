from airflow.sensors.filesystem import FileSensor
from airflow import DAG
import pendulum


with DAG(
    dag_id = 'dag_file_sensor',
    start_date = pendulum.datetime(2024,12,16, tz='Asia/Seoul'),
    schedule='0 6 * * *',
    catchup=False
) as dag:
    
    tvCorona19VaccinestatNew_sensor = FileSensor(
        task_id = 'tvCorona19VaccinestatNew_sensor',
        fs_conn_id = 'conn_file_opt_airflow_files',
        filepath='tvCorona19VaccinestatNew/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}/tvCorona19VaccinestatNew.csv',
        recursive=False,
        poke_interval = 10,
        timeout=60*2,
        #timeout=60*60*24, #1일
        mode='reschedule'
    )