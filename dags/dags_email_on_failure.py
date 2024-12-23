from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from airflow.exceptions import AirflowException
import pendulum
from datetime import timedelta
from airflow.models import Variable

# 아래 2줄은 Dag을 파싱하는 과정에서 스케줄러의 부하를 줄 수 있지만, 모니터링 관점에서는 유용할 수 있다
# DAG 위에 작성한다고, 즉 스케줄러가 계속 파싱한다고 부정적으로 생각하지 말고
# Trade-off 잘 생각해보고 결정하자
email_str = Variable.get("email_target")
email_lst = [email.strip() for email in email_str.split(',')]

with DAG(
    dag_id='dags_email_on_failure',
    start_date=pendulum.datetime(2024,12,23, tz='Asia/Seoul'),
    catchup=False,
    schedule='0 1 * * *',
    dagrun_timeout=timedelta(minutes=2),
    default_args={ # 모든 Task의 공통 파라미터
        'email_on_failure': True, # 실패시 메일로 알람을 보냄
        'email': email_lst
    }
) as dag:
    
    @task(task_id = 'python_fail')
    def python_task_func():
        raise AirflowException('에러 발생')
    
    python_task_func()

    bash_fail = BashOperator(
        task_id = 'bash_fail',
        bash_command= = 'exit 1'

    )
    bash_success = BashOperator(
        task_id = 'bash_success',
        bash_command='exit 0'
    )