import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable

with DAG(
    dag_id="dags_bash_with_variable", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="30 6 * * *",
    start_date=pendulum.datetime(2024, 12, 10, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
) as dag:
    var_value = Variable.get("sample_key") # 미권고

    bash_var_1 = BashOperator(
        task_id = 'bash_var_1',
        bash_command = f"echo variable_1 : {var_value}"
    )

    bash_var_2 = BashOperator( # 추천
        task_id = 'bash_var_2',
        bash_command = f"echo variable_2 : {{var.value.sample_key}}" # var.value 부분은 공통
    )

    bash_var_1 >> bash_var_2