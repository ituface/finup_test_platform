from django.shortcuts import render, render_to_response, HttpResponse
from public import Decorator
from public.mysql import MysqlHandle
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import os, time
import shutil
from  AppManage.CreatePlist import createplist
from public.send_email import send_email

'''
app列表
'''
import json


@csrf_exempt
@Decorator.get_web_input_data('app_list_select')
@Decorator.Handle_time
def app_list(request):
    sql = request.DPOST.get('sql') + ' order by create_time desc'

    MysqlHandle.reConnect()
    data = MysqlHandle.select_mysql_data(sql)

    paginator = Paginator(data, 10)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return render(request, 'app-list.html', {'applist': result, 'paginator': paginator})


'''

app删除

'''


@require_POST
@csrf_exempt
def del_app_list(request):
    column_id = request.POST['column_id']
    MysqlHandle.reConnect()
    sql_del = MysqlHandle.get_xml_sql(xml_path='delete_sql', xml_tag='delete', xml_id='delete_app_list_id')  # 删除app的sql
    sql_path = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select',
                                       xml_id='delete_file_path')  # 查找app路径的sql
    data = MysqlHandle.select_mysql_data(sql_path.format(id=column_id))[0];
    app_path = data.get('appPath')
    app_path = './static/' + app_path[:18]
    try:
        shutil.rmtree(app_path)
    except Exception as e:
        tag = 2
    tag = MysqlHandle.delete_update_insert_mysql_data(sql_del.format(id=column_id))

    if tag == 1:
        return HttpResponse('1')
    elif tag == 2:
        return HttpResponse('2')
    else:
        return HttpResponse('0')


'''
app上传
'''


@csrf_exempt
def add_app(request):
    timestrap = str(int(time.time()));
    sql = MysqlHandle.get_xml_sql(xml_path='insert_sql', xml_id='insert_app_path', xml_tag='insert')
    Rootpath = './static/appfile/{timestrap}/'.format(timestrap=timestrap)
    myFilemessage = ''
    print('request-----》', request.POST)
    if request.method == 'POST':
        myFile = request.FILES.get('myfile')

        customerOruser = request.POST.get('customerOruser')

        appType = request.POST.get('app_type')
        isfinal = request.POST.get('isfinal')
        app_version = request.POST.get('app_version')
        appPath = Rootpath + myFile.name
        os.makedirs(Rootpath)
        describe = request.POST.get('describe')
        environment = request.POST.get('environment')
        test_or_beta = request.POST.get('test_or_beta')
        #发送邮件所用标题
        title = "{environment}-{appType}-{customerOruser}".format(environment=environment, appType=appType,
                                                                  customerOruser=customerOruser)
        #发送邮件所用名单

        email_list=['yelishuan@finupgroup.com','quguangwen@finupgroup.com']

        describe = describe if describe else ''
        customerOruser = 'USER' if customerOruser == '钢铁侠' else 'CUSTOMER'
        isfinal = 1 if isfinal == '是' else 0
        if appType == "ANDROID":
            qr_path = appPath[9:]
        elif appType == "IOS":
            tag = createplist(appPath.lstrip('.'), timestrap)
            if tag == '1':
                qr_path = 'https://gitee.com/ituface/test/raw/master/%s.plist' % timestrap
            else:
                myFilemessage = '上传失败了'

        if not myFile:
            return render(request, 'order-add.html', {'myFilemessage': '文件有误，请重新上传'})
        destination = open(os.path.join(Rootpath, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        try:
            sql = sql.format(appVersion=app_version, appType=appType, customerOruser=customerOruser, describe=describe,
                             appPath=appPath[9:], environment=environment, isFinal=isfinal, test_or_beta=test_or_beta,
                             qr_path=qr_path)
            print('sql---->', sql)
            MysqlHandle.reConnect()
            sta = MysqlHandle.delete_update_insert_mysql_data(sql)
            if sta != 1:
                myFilemessage = '上传失败了'
        except Exception:
            myFilemessage = '上传失败'
            sta = 2
        if sta == 1:
            myFilemessage = '上传成功'
            send_email(email_list,title,"描述：%s"%describe)

    return render(request, 'add-app.html', {'myFilemessage': myFilemessage})


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def update_app(request):
    ids = request.GET['id']

    sql_select = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='update_app_list')
    MysqlHandle.reConnect()
    data = MysqlHandle.select_mysql_data(sql_select.format(id=ids))[0]
    data['describe'] = data['describe'].replace("\r\n", "\\n")
    message = ''
    if request.method == 'POST':
        appType = request.POST.get('app_type')
        environment = request.POST.get('environment')
        customeroruser = request.POST.get('customeroruser')
        isfinal = request.POST.get('isfinal')
        app_version = request.POST.get('app_version')
        describe = request.POST.get('describe')
        test_or_beta = request.POST.get('test_or_beta')
        sql = MysqlHandle.get_xml_sql(xml_path='update_sql', xml_tag='update', xml_id='update_app_manage')
        tag = MysqlHandle.delete_update_insert_mysql_data(
            sql.format(appType=appType, environment=environment, customerOruser=customeroruser,
                       isFinal=isfinal, appVersion=app_version, describe=describe, test_or_beta=test_or_beta, id=ids))
        if tag == 0 or tag == 1:
            MysqlHandle.reConnect()
            data = MysqlHandle.select_mysql_data(sql_select.format(id=ids))[0]
            message = '修改成功！'
        else:
            message = '修改失败！'

    return render(request, 'update_app.html', {'data': data, 'message': message})


def qr_ios_download(request):
    ids = request.GET['id']
    sql_select = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_ios_qr_path')
    data = MysqlHandle.select_mysql_data(sql_select.format(id=ids))[0]

    return render(request, 'qr-ios-download.html', {'data': data})


def finup_lottery(request):
    return render(request, 'finup-lottery.html')
