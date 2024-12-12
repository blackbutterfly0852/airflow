import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.providers.http.operators.http import SimpleHttpOperator

with DAG(
    dag_id="dags_simple_http_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule=None,
    start_date=pendulum.datetime(2024, 12, 13, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    ''' 서울시 부동산 실거래가 정보 '''
    tb_Ln_Opendata_rtmsV = SimpleHttpOperator(
        task_id = 'tb_Ln_Opendata_rtmsV',
        http_conn_id = 'openapi.seoul.go.kr',
        endpoint = '{{var.value.apikey_openapi_seoul_go_kr}}/json/tbLnOpendataRtmsV/1/10/',
        method = 'GET',
        header = {'Content-Type':'application/json',
                  'charset' : 'utf-8',
                  'Accpet' : '*/*'}
    )

    @task(task_id = 'python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids = 'tb_Ln_Opendata_rtmsV')
        import json
        from pprint import pprint

        pprint(json.load(rslt))
    
    tb_Ln_Opendata_rtmsV >> python_2()