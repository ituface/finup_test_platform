from django.shortcuts import render
from django.shortcuts import render, render_to_response, HttpResponse
from public import Decorator
from public.mysql import MysqlHandle
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import os, time
import datetime
import json
from django.utils.safestring import mark_safe

from  AppManage.CreatePlist import createplist


# Create your views here.

def index(request):
    from django.core.cache import cache
    cache.set('click_count',0)
    cache.incr('click_count')
    print('redis'*30,cache.get('click_count'))
    return render(request, 'index.html')


def welcome(request):
    date = []
    app_count = []
    piece_count = []
    # 计算一周前今天的日期
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-7)
    hebdomad_ago = (today + offset).strftime('%Y-%m-%d')
    print('一周前的今天', hebdomad_ago)
    sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_statistics_amount_app_data')
    data = MysqlHandle.select_mysql_data(sql.format(hebdomad_ago=hebdomad_ago))
    for i in data:
        date.append(i['date'])
        app_count.append(i['count'])

    # 查询进件数
    piece_sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select',
                                        xml_id='select_statistics_amount_piece_data')
    piece_data = MysqlHandle.select_mysql_data(piece_sql.format(hebdomad_ago=hebdomad_ago))
    for i in piece_data:
        piece_count.append(i['count'])
    result = {'date': mark_safe(date), 'piece_count': piece_count, 'app_count': app_count}
    print('result=======>', result)
    return render(request, 'welcome.html', result)
