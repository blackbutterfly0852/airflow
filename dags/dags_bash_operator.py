import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dags_bash_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 11, 27, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    #dagrun_timeout=datetime.timedelta(minutes=60),
    #tags=["example", "example2"],
    #params={"example_key": "example_value"}, # task 내 공통적으로 전달한 파라미터
)  as dag:
    # [START howto_operator_bash]
    bash_t1 = BashOperator( # 오퍼레이터가 테스크를 생성
        task_id="bash_t1", # 테스크명과 일치
        bash_command="echo whoami",
    )

    bash_t2 = BashOperator( # 오퍼레이터가 테스크를 생성
        task_id="bash_t2", # 테스크명과 일치
        bash_command="echo $HOSTNAME",
    )

    bash_t1 >> bash_t2