from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum
from airflow.models import Variable

email_str = Variable.get('email_target')
email_lst = [email.strip() for email in email_str.split(',')]

with DAG(
    dag_id = 'dags_sla_email_example',
    start_date=pendulum.datetime(2024, 12, 25, tz='Asia/Seoul'),
    schedule='*/10 * * * *', # 10분마다
    catchup=False,
    default_args={ # 오퍼레이터 수준
        'sla': timedelta(seconds=70),
        'email': email_lst
    }
) as dag:
    
    task_slp_30s_sla_70s = BashOperator(
        task_id = 'task_slp_30s_sla_70s',
        bash_command= 'sleep 30'
    )

    task_slp_60s_sla_70s = BashOperator(
        task_id = 'task_slp_60s_sla_70s',
        bash_command= 'sleep 60'
    )

    task_slp_10s_sla_70s = BashOperator( # 시작도 하기 전 Miss
        task_id = 'task_slp_10s_sla_70s',
        bash_command= 'sleep 10'
    )

    task_slp_10s_sla_30s = BashOperator( # 시갖도 하기 전 Miss
        task_id = 'task_slp_10s_sla_30s',
        bash_command= 'sleep 10',
        sla=timedelta(seconds=30)
    )
    task_slp_30s_sla_70s >> task_slp_60s_sla_70s >> task_slp_10s_sla_70s >> task_slp_10s_sla_30s


