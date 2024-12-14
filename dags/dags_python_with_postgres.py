import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import random

with DAG(
    dag_id="dags_python_with_postgres", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 9 * * *",
    start_date=pendulum.datetime(2024, 12, 14, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    
    def insert_postgres(ip, port, dbname, user, passwd, **kwargs):
        import psycopg2
        from contextlib import closing
        # psycopg2.connect ~~ : DB서버와의 연결 (session)
        # 1번 closing : conn.close() 역할
        with closing(psycopg2.connect(host=ip, dbname=dbname, user=user, password=passwd, port=int(port))) as conn:
            # cursor : session 내에서 쿼리를 수행하고 결과를 받아올 수 있는 역할, session을 통해 cursor를 생성하고, cursor를 통해 sql를 수행
            with closing(conn.cursor()) as cursor:
                dag_id = kwargs.get('ti').dag_id
                task_id = kwargs.get('ti').task_id
                run_id = kwargs.get('ti').run_id
                msg = 'insert 수행'
                sql = 'insert into py_opr_drct_insert values (%s,%s,%s,%s);'
                cursor.execute(sql, (dag_id, task_id, run_id, msg))
                conn.commit()

    insert_postgres = PythonOperator(
        task_id = 'insert_postgres',
        python_callable=insert_postgres,
        op_args=['172.28.0.3', '5432','dwkim','dwkim','dwkim']
    )
    # hook 사용
    # 위 코드의 문제점 : 접속정보 노출문제, 접속정보 변경 문제 > Dag이 여러개라면?
    def insert_postgres_with_hook(postgres_conn_id, **kwargs):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from contextlib import closing
        postgres_hook = PostgresHook(postgres_conn_id)
        with closing(postgres_hook.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                dag_id = kwargs.get('ti').dag_id
                task_id = kwargs.get('ti').task_id
                run_id = kwargs.get('ti').run_id
                msg = 'insert 수행_hook'
                sql = 'insert into py_opr_drct_insert values (%s,%s,%s,%s);'
                cursor.execute(sql, (dag_id, task_id, run_id, msg))
                conn.commit()

    insert_postgres_with_hook = PythonOperator(
        task_id = 'insert_postgres_with_hook',
        python_callable=insert_postgres_with_hook,
        op_kwargs={'postgres_conn_id' : 'conn-db-postgres-custom'}
    )
    insert_postgres >> insert_postgres_with_hook
