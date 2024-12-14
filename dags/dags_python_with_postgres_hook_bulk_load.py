import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
    dag_id="dags_python_with_postgres_hook_bulk_load", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 7 * * *",
    start_date=pendulum.datetime(2024, 12, 14, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    def insert_postgres(postgres_conn_id, tbl_nm, file_nm, **kwargs):
        postgres_hook = PostgresHook(postgres_conn_id)
        postgres_hook.bulk_load(tbl_nm, file_nm)

    insert_postgres = PythonOperator(
        task_id = 'insert_postgres',
        python_callable=insert_postgres,
        op_kwargs={ 'postgres_conn_id' : 'conn-db-postgres-custom',
                   'tbl_nm' : 'TbCorona19CountStatus_bulk1',
                   'file_nm' : '/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash}}/TbCorona19CountStatus.csv'
                   }
    )

    insert_postgres