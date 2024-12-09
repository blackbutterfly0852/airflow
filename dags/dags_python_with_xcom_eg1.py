import pendulum
from airflow.models.dag import DAG
from airflow.decorators import task


with DAG(
    dag_id="dags_python_with_xcom_eg1", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 9, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
) as dag:
    @task(task_id = 'python_xcom_push_task1')
    def xcom_push1(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key = 'result1', value = "value_1")
        ti.xcom_push(key = 'result2', value = [1,2,3])

    @task(task_id = 'python_xcom_push_task2')
    def xcom_push2(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push(key = "result1", value = "value_2")
        ti.xcom_push(key = "result2", value = [1,2,3,4])

    @task(task_id = 'python_xcom_pull_task')
    def xcom_pull(**kwargs):
        ti = kwargs['ti']
        value1 = ti.xcom_pull(key = "result1")
        value2 = ti.xcom_pull(key = "result2", task_id = 'python_xcom_push_task1')
        print(value1)
        print(value2)

    xcom_push1() >> xcom_push2() >> xcom_pull()