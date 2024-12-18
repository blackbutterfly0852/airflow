import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.decorators import task

with DAG(
    dag_id='dags_branch_python_operator',
    start_date=pendulum.datetime(2024,12,17, tz='Asia/Seoul'), 
    schedule='0 1 * * *',
    catchup=True
) as dag:   
    
    def select_random():
        import random

        item_list = ['A','B','C']
        selected_item = random.choice(item_list)
        print('selected_item', selected_item)
        if selected_item == 'A':
            return 'task_a' # 실제 task_id 작성
        elif selected_item in ['B', 'C']:
            return ['task_b', 'task_c']

    python_branch_task = BranchPythonOperator (
        task_id = 'python_branch_task',
        python_callable = select_random
    )


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

    python_branch_task >> [task_a, task_b, task_c]