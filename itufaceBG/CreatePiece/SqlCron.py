import multiprocessing
from apscheduler.schedulers.blocking import BlockingScheduler
from public.mysql import MysqlHandle
import datetime
'''
带参
'''
def scheduler(parameter):
    def outer(func):
        def inner(*args, **kwargs):
            def worker():
                scheduler = BlockingScheduler()
                scheduler.add_job(func=func, trigger='cron', hour=10,minute = 0,second=0)
                scheduler.start()
            p = multiprocessing.Process(target=worker, args=())
            print('pa-',parameter)
            p.start()
        return inner
    return outer

'''
不带参
'''


def schedulers(func):
    def inner():
        def worker():
            scheduler = BlockingScheduler()
            scheduler.add_job(func=func, trigger='cron',hour=16,minute =20,second=0)
            scheduler.start()
        p = multiprocessing.Process(target=worker, args=())
        p.start()
    return inner
def testschedulers(func):
    def inner():
        def worker():
            scheduler = BlockingScheduler()
            scheduler.add_job(func=func, trigger='cron',hour=19,minute =25,second=0)
            scheduler.start()
        p = multiprocessing.Process(target=worker, args=())
        p.start()
    return inner

@schedulers
def update_city_code():
        print('datetime------>',datetime.datetime.now())
        sql=MysqlHandle.get_xml_sql(xml_path='update_sql',xml_tag='update',xml_id='timer_regions')
        MysqlHandle.delete_update_insert_mysql_data(sql)

@schedulers
def insert_statistics_amount():
    # 计算昨天日期
    print('开始了')
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-1)
    yesterday = (today + offset).strftime('%Y-%m-%d')
    # 查询昨日造件数量
    piece_sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_chart_piece')
    piece_data = MysqlHandle.select_mysql_data(piece_sql.format(create_time=yesterday))
    piece_number = piece_data[0].get('number')
    print(
        'piece_data---->',piece_data
    )
    # 查询昨日上传包数量
    app_sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_chart_app')
    app_data = MysqlHandle.select_mysql_data(app_sql.format(create_time=yesterday))
    app_number = app_data[0].get('number')
    print(
        'app_number---->', app_number
    )

    # 将数量插入到statistics_amount中
    statistics_tuple = ((piece_number, 'PIECE'), (app_number, 'APP'))
    statistics_sql = MysqlHandle.get_xml_sql(xml_path='insert_sql', xml_tag='insert',
                                             xml_id='insert_into_statistics_data')
    for inner in statistics_tuple:
       tag= MysqlHandle.delete_update_insert_mysql_data(
            statistics_sql.format(date_record=yesterday, count=inner[0], category=inner[1]))
       print('tag----->',tag)
