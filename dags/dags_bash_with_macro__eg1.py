import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dags_bash_with_macro__eg1", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="10 0 L * *", # 매월 말일에 수행되는 배치
    start_date=pendulum.datetime(2024, 12, 1, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    # STAET_DATE : 전월 말일, END_DATE : 1일전 (매월 말일 - 1일)
    bask_task_1 = BashOperator(
        task_id = 'bask_task_1',
        env={
            'START_DATE' : '{{ data_interval_start.in_timezone("Asia/Seoul") | ds}}',
            'END_DATE' : '{{ ( data_interval_end.in_timezone("Asia/Seoul") - macros.dateutil.relativedelta.relativedelta(days=1) ) | ds}}'
        },
        bash_command=' echo "START_DATE : $START_DATE" && echo "END_DATE : $END_DATE" '
    )