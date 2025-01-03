from airflow import Dataset
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum



dataset_dags_dataset_producer_2 = Dataset("dags_dataset_producer_2") # produce 시 key값

with DAG(
        dag_id='dags_dataset_producer_2',
        schedule='0 7 * * *',
        start_date=pendulum.datetime(2024, 12, 23, tz='Asia/Seoul'),
        catchup=False
) as dag:
    
    bash_task = BashOperator(

        task_id = 'bash_task',
        outlets = [dataset_dags_dataset_producer_2], # BaseOperator 내 parameter, 해당 task가 종료되면, dataset_dags_dataset_producer_2 produce 함
        bash_command= 'echo "producer_2 수행완료" '
    )