from airflow import DAG
from airflow.sensors.python import PythonSensor
import pendulum
from airflow.hooks.base import BaseHook

with DAG(
    dag_id='dags_python_sensor',
    start_date=pendulum.datetime(2024,12,17, tz='Asia/Seoul'),
    schedule='10 1 * * *',
    catchup=False
) as dag:
    
    def check_api_update(http_conn_id, endpoint, base_dt_col, **kwargs):
        
        import requests
        import json
        from dateutil import relativedelta
        from pprint import pprint
        
        connection = BaseHook.get_connection(http_conn_id)
        url = f'{connection.host}:{connection.port}/{endpoint}/1/100/'
        response = requests.get(url)
        
        contents = json.loads(response.text)
        print('--contents--')
        pprint(contents)
        key_nm = list(contents.keys())[0]
        print('--ket_nm--')
        pprint(key_nm)
        row_data = contents.get(key_nm).get('row')
        print('--row_data--')
        pprint(row_data)
        last_dt = row_data[0].get(base_dt_col)
        last_date = last_dt[:10]
        last_date = last_date.replace('.','-').replace('/','-')
        print('last_date : ', last_date)
        today_ymd = kwargs.get('data_interval_end').in_timezone('Asia/Seoul').strftime('%Y-%m-%d')
        try:
            last_date = pendulum.from_format(last_date, 'YYYY-MM-DD')
        except:
            from airflow.exceptions import AirflowException
            AirflowException(f'{base_dt_col} 컬럼은 YYYY.MM.DD 또는 YYYY/MM/DD 형태가 아닙니다.')
        print(last_date)
        print(today_ymd)
        if last_date >= today_ymd:
            print(f'생성 확인(배치 날짜: {today_ymd} / API Last 날짜: {last_date})')
            return True
        else:
            print(f'미완료(배치 날짜: {today_ymd} / API Last 날짜: {last_date})')
            return False

    sensor_task = PythonSensor(
        task_id = 'sensor_task',
        python_callable=check_api_update,
        op_kwargs = {
            'http_conn_id' : 'openapi.seoul.go.kr',
            'endpoint' : '{{var.value.apikey_openapi_seoul_go_kr}}/json/SPOP_LOCAL_RESD_DONG', # 행정동 단위 서울 생활인구(내국인)
            'base_dt_col' : 'STDR_DE_ID'
        },
        poke_interval = 600, # 10분
        mode = 'reschedule'
    )
    
    sensor_task


