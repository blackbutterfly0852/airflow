import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dags_bash_with_template", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="10 0 * * *",
    start_date=pendulum.datetime(2024, 12, 4, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    
    base_t1 = BashOperator(
        task_id = 'base_t1',
        bash_command='echo "data_interval_end: {{ data_interval_end }} "'
    )

    base_t2 = BashOperator(

        task_id = 'base_t2',
        env = {
            'START_DATE' : '{{ data_interval_start | ds }}',
            'END_DATE' : '{{ data_interval_end | ds }}'
        },
        bash_command='echo $START_DATE && $END_DATE'
    )

    base_t1 >> base_t2