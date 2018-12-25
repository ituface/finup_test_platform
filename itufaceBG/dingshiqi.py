# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def aps_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)

scheduler = BlockingScheduler()
scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5')
scheduler.start()