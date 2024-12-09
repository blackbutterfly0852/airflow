import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="dags_bash_with_xcom", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 11, 27, tz="Asia/Seoul"),
    catchup=False
)  as dag:
    
    bash_push = BashOperator(
        task_id = 'bash_push',
        bash_command="echo START && "
                     "echo XCOM_PUSHED "
                     " {{ ti.xcom_push(key = 'bash_pushed', value ='first_bash_message') }} && "
                     "echo COMPLETE"
    )

    bash_pull = BashOperator(
        task_id = 'bash_pull',
        env = { 'PUSHED_VALUE' : " {{ ti.xcom_pull(key = 'bash_pushed') }} ", # key값으로 value값 출력
                'RETURN_VALUE' : " {{ ti.xcom_pull(task_ids = 'bash_push') }} " }, # 마지막 echo문 출력
        bash_command="echo $PUSHED_VALUE && echo $RETURN_VALUE",
        do_xcom_push=False # 출력문을 자동으로 xcom에 올리는 것 금지 
    )

    bash_push >> bash_pull