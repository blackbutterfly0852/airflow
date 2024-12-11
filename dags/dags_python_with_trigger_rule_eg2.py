import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from airflow.exceptions import AirflowException

with DAG(
    dag_id="dags_python_with_trigger_rule_eg2", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2024, 12, 11, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)

)  as dag:
    @task.branch(task_id = 'branching')
    def random_branch():
        import random
        item_list = ['A',' B', 'C']
        selected_item = random.choice(item_list)
        
        if selected_item == 'A':
            return 'task_a' # 실제 task_id 작성
        elif selected_item in ['B', 'C']:
            return ['task_b', 'task_c']

    @task(task_id = 'task_a')
    def task_a():
        print('task_a')

    @task(task_id = 'task_b')
    def task_b():
        print('task_b')

    @task(task_id = 'task_c')
    def task_c():
        print('task_c')
        
    @task(task_id = 'task_d', trigger_rule = 'none_skipped') # Skip 된 상위 Task가 없으면 실행 (상위 Task가 성공, 실패여도 무방)
    def task_d():
        print('task_d')
    
    random_branch() >> [task_a(), task_b(), task_c()] >> task_d()


    
    