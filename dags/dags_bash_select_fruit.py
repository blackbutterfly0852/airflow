import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dags_bash_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="10 0 * * 6#1",
    start_date=pendulum.datetime(2024, 11, 28, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    t1_orange = BashOperator( # 오퍼레이터가 테스크를 생성
        task_id="t1_orange", # 테스크명과 일치
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh ORANGE",
    )

    t2_avocado = BashOperator( # 오퍼레이터가 테스크를 생성
        task_id="t2_avocado", # 테스크명과 일치
        bash_command="/opt/airflow/plugins/shell/select_fruit.sh AVOCADO",
    )

    t1_orange >> t2_avocado