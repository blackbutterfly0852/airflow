import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

with DAG(
    dag_id="dags_bash_python_with_xcom", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 10, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
) as dag:
    @task(task_id='python_push')
    def python_push_xcom():
        result_dict = {'status' : 'good', 'data' : [1,2,3], 'options_cnt' : 100}
        return result_dict

    bash_pull = BashOperator(
        task_id = 'bash_pull',
        env = {
            'STATUS' : '{{ ti.xcom_pull(task_ids = "python_push")["status"] }}',
            'DATA' : '{{ ti.xcom_pull(task_ids = "python_push")["status"] }}',
            'OPTIONS_CNT' : '{{ ti.xcom_pull(task_ids = "python_push")["options_cnt"] }}'

        },
        bash_command = 'echo $STATUS && echo $DATA && echo $OPTIONS_CNT'
    )

    python_push_xcom() >> bash_pull

    bash_push = BashOperator(
         task_id = 'bash_push',
         bash_command = 'echo PUSH START '
                        '{{ ti.xcom_push(key = "bash_pushed", value = 200) }} && '
                        'echo PUSH_COMPLETE'
    )

    @task(task_id='python_pull')
    def python_pull_xcom(**kwargs):
        ti = kwargs['ti']
        status_value = ti.xcom_pull(key = 'bash_pushed')
        return_value = ti.xcom_pull(task_ids = 'bash_push')
        print('status_value : ' + str(status_value))
        print('return_value : ' + return_value)

    bash_push >> python_pull_xcom()