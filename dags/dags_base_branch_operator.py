import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.branch import BaseBranchOperator
from airflow.decorators import task

with DAG(
    dag_id="dags_base_branch_operator", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 11, tz="Asia/Seoul"),
    catchup=False, # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    
    class CustomBranchOperator(BaseBranchOperator): # 다중 상속이 가능하나, 한 개의 클래스만 상속 받는 것을 권고
        def choose_branch(self, context): # choose_branch 이름 및 context( == **kwargs) 그대로 사용필요
            import random
            print(context)
            item_list = ['A',' B', 'C']
            selected_item = random.choice(item_list)
        
            if selected_item == 'A':
                return 'task_a' # 실제 task_id 작성
            elif selected_item in ['B', 'C']:
                return ['task_b', 'task_c']
        
    
    
        
    custom_branch_operator = CustomBranchOperator(task_id = 'python_branch_task')
    
    def common_func(**kwargs):
        print(kwargs['selected'])


    task_a = PythonOperator (
        task_id = 'task_a',
        python_callable = common_func,
        op_kwargs = {'selected' : 'A'}
    )

    task_b = PythonOperator (
        task_id = 'task_b',
        python_callable = common_func,
        op_kwargs = {'selected' : 'B'}
    )

    task_c = PythonOperator (
        task_id = 'task_c',
        python_callable = common_func,
        op_kwargs = {'selected' : 'C'}
    )

    custom_branch_operator >> [task_a, task_b, task_c]



