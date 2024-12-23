from airflow import Dataset
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

dataset_dags_dataset_producer_1 = Dataset("dags_dataset_producer_1")
dataset_dags_dataset_producer_2 = Dataset("dags_dataset_producer_2")

with DAG(
        dag_id='dags_dataset_consumer_2',
        schedule=[dataset_dags_dataset_producer_1,dataset_dags_dataset_producer_2], # dataset_dags_dataset_producer_1/2에 produce(trigger)가 되면 스케줄 시작
        start_date=pendulum.datetime(2024, 12, 23, tz='Asia/Seoul'),
        catchup=False
) as dag:
    
    bash_task = BashOperator(
        task_id = 'bash_task',
        bash_command='echo {{ ti.run_id }} && echo "produce_1 와 produce_2 완료되면 수행" '
    )