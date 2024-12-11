import pendulum
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label

with DAG (
    dag_id="dags_empty_with_edge_label", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 12, 11, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)

) as dag:

    empty_1 = EmptyOperator(
        task_id = 'empty_1'
    )

    empty_2 = EmptyOperator(
        task_id = 'empty_2'
    )

    empty_1 >> Label('1과 2사이') >> empty_2

    empty_3 = EmptyOperator(
        task_id = 'empty_3'
    )

    empty_4 = EmptyOperator(
        task_id = 'empty_4'
    )

    empty_5 = EmptyOperator(
        task_id = 'empty_5'
    )

    empty_6 = EmptyOperator(
        task_id = 'empty_6'
    )

    empty_2 >> Label('Start Branch') >> [empty_3, empty_4, empty_5] >> Label('End Branch') >> empty_6