from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import timedelta
from airflow.models import Variable

email_str = Variable.get("email_target")
email_lst = [email.strip() for email in email_str.split(',')]

with DAG(
    dag_id='dags_timeout_example_2',
    start_date=pendulum.datetime(2023, 5, 1, tz='Asia/Seoul'),
    catchup=False,
    schedule=None,
    dagrun_timeout=timedelta(minutes=1),
    default_args={
        'execution_timeout': timedelta(seconds=40),
        'email_on_failure': True, # operator 수준(Task) 이라 dag이 fail이어도 email 발송 x
        'email': email_lst
    }
) as dag:
    bash_sleep_35 = BashOperator(
        task_id='bash_sleep_35',
        bash_command='sleep 35',
    )

    bash_sleep_36 = BashOperator( # Skipped : Dag run timeout시 수행하고 있는 Task
        trigger_rule='all_done',
        task_id='bash_sleep_36',
        bash_command='sleep 36',
    )

    bash_go = BashOperator( # no Status : Dag run timeout시 수행되지 않은 후행 Task
        task_id='bash_go',
        bash_command='exit 0',
    )

    bash_sleep_35 >> bash_sleep_36 >> bash_go