# from 모듈 or 패키지 > 어디서 가져올지
# import 함수, 클래스, 변수 > 무엇을 가져올지
# 모듈 : 파이썬 코드가 작성된 단일 파일, .py 확장자를 가진 파일
# 패키지 : 패키지는 모듈들을 포함한 디렉토리
from airflow import DAG
import pendulum
import datetime
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="dags_conn_test", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule=None,
    start_date=pendulum.datetime(2024, 11, 28, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
    
)  as dag:
    # [START howto_operator_bash]
    t1 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t1" # 테스크명과 일치
    )

    t2 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t2" # 테스크명과 일치
    )

    t3 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t3" # 테스크명과 일치
    )

    t4 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t4" # 테스크명과 일치
    )

    t5 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t5" # 테스크명과 일치
    )

    t6 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t6" # 테스크명과 일치
    )

    t7 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t7" # 테스크명과 일치
    )

    t8 = EmptyOperator( # 오퍼레이터가 테스크를 생성
        task_id="t8" # 테스크명과 일치
    )

    t1 >> [t2, t3] >> t4
    t5 >> t4
    [t4, t7] >> t6 >> t8
