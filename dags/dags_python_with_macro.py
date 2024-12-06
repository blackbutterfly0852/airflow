from airflow import DAG
import pendulum
from airflow.decorators import task
# 스케줄러가 주기적으로 문법적 오류를 검사하는 위치
with DAG(
    dag_id="dags_python_with_macro", # 일반적으로 DagId와 파일명과 일치시키는것이 좋음
    schedule="10 0 * * *",
    start_date=pendulum.datetime(2024, 12, 6, tz="Asia/Seoul"),
    catchup=False # 일반적으로 false, 누락된 구간을 동시에 수행(순차적이 아님)
  
)  as dag:
    # 스케줄러가 주기적으로 문법적 오류를 검사하는 위치 
    # start_date : 전달 1일, end_date :  전달 말일
    @task(task_id = 'task_using_macros',
          templates_dict= { 'start_date' : '{{ ( data_interval_end.in_timezone("Asia/Seoul") + macros.dateutil.relativedelta.relativedelta(months=-1, day=1) ) | ds }}',
                        'end_date' :  '{{ ( data_interval_end.in_timezone("Asia/Seoul").replace(day=1) + macros.dateutil.relativedelta.relativedelta(days=-1) ) | ds }}' } )
    # templates_dict >> **kwargs 
    def get_datetime_macro(**kwargs):
        templates_dict = kwargs.get('templates_dict') or {}
        if templates_dict:
            start_date = templates_dict.get('start_date') or 'start_date 없음'
            end_date = templates_dict.get('end_date') or 'end_date 없음'
            print('### get_datetime_macro_start ###')
            print('start_date : ' + start_date)
            print('end_date : ' + end_date)
            print('### get_datetime_macro_end ###')

    @task(task_id= 'task_direct_calc')
    def get_datetime_calc(**kwargs):
        from dateutil.relativedelta import relativedelta # 스케줄러의 부하 경감을 위해 task_decorator 혹은 operator 내에 작성
        data_interval_end = kwargs['data_interval_end']
        prev_month_first = data_interval_end.in_timezone('Asia/Seoul') + relativedelta(months=-1, day=1)
        prev_month_last = data_interval_end.in_timezone('Asia/Seoul').replace(day=1) + relativedelta(days=-1)
        print('### get_datetime_calc_start ###')
        print(prev_month_first.strftime('%Y-%m-%d'))
        print(prev_month_last.strftime('%Y-%m-%d'))
        print('### get_datetime_calc_end ###')

    get_datetime_macro() >> get_datetime_calc()