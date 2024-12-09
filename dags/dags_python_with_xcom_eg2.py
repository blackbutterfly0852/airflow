import pendulum
from airflow.models.dag import DAG
from airflow.decorators import task


with DAG(
    dag_id="dags_python_with_xcom_eg1", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 9, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
) as dag:
    @task(task_id = 'python_xcom_push_by_return')
    def xcom_push_result(**kwargs):
        return 'Success'

    @task(task_id = 'python_xcom_pull_1')
    def xcom_pull_1(**kwargs):
        ti = kwargs['ti']
        value1 = ti.xcom_pull(task_ids='python_xcom_push_by_return')
        print(value1)

    @task(task_id = 'python_xcom_pull_2')
    def xcom_pull_2(status, **kwargs):
        print('함수입력값으로 받은 값 : ' + status)

    python_xcom_push_by_return = xcom_push_result()
    xcom_pull_2(python_xcom_push_by_return)
    python_xcom_push_by_return >> xcom_pull_1()
