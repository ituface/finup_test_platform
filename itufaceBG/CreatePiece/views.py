#coding:utf-8
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt
import time, json
import requests
from  CreatePiece.api.stauts import status as Func_status
from public.mysql import MysqlHandle
from public.path import path
from public.Decorator import RequestPostToStr
from public.Decorator import get_web_input_data
from public.Decorator import Handle_time
from CreatePiece.api.GetRequest import GetRequest
from django.http import JsonResponse
import bisect
from CreatePiece.api.AddPiece import AddPiece
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# 接口地址

@csrf_exempt
@get_web_input_data('select_piece_list')
@Handle_time
def piece_list(request):
    print('post----------->', request.POST)
    sql = request.DPOST.get('sql') + ' order by create_time desc'
    data = MysqlHandle.select_mysql_data(sql)
    print('sqls------>', sql)
    paginator = Paginator(data, 20)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return render(request, 'piece-list.html', {'piecelist': result, 'paginator': paginator})


@csrf_exempt
def add_piece(request):
    sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_product_list')
    data = MysqlHandle.select_mysql_data(sql)
    return render(request, 'add-piece.html', {'data': data})


'''
产品列表
'''


@csrf_exempt
def app_product(request):
    sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_product_list')
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
    return render(request, 'app-product.html', {'data': result, 'paginator': paginator})


'''
添加产品
'''


@csrf_exempt
def add_product(request):
    message = ''
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_enum = request.POST['product_enum']
        product_type = request.POST['product_type']
        sql = MysqlHandle.get_xml_sql(xml_path='insert_sql', xml_tag='insert', xml_id='insert_app_product')
        sql = sql.format(product_name=product_name, product_enum=product_enum, product_type=product_type)
        tag = MysqlHandle.delete_update_insert_mysql_data(sql)
        if tag == 1:
            message = '添加成功'
        else:
            message = '添加失败'

    return render(request, 'add-product.html', {'message': message})


'''
新增进件处理api
'''


@csrf_exempt
@RequestPostToStr(['num', 'status'])
def add_piece_api(request):
    gain_data = request.POST
    status = gain_data['status']
    num = gain_data['num']
    name = gain_data['name']
    product_type = gain_data['product_type']
    video_check = gain_data['video_check']
    print('video_Check--------------->', video_check)
    print('gain_data---->', gain_data)
    mobile = gain_data['mobile']
    lend_status = Func_status('lend')
    print('status---------------->', status)
    if status in lend_status and num == '0' and product_type == '':  # 判断是否需要搜索进件
        data = {'status': status}
        result = post(url='/v1/get/SearchResult', data=data)
        print('result------>', result)
        if result:
            return HttpResponse(result, content_type="application/json")

    mobile_enable = AddPiece.mobile_enable(mobile)  # 判断手机号是否有人使用
    if mobile_enable:
        return JsonResponse({'code': 202, 'message': '手机号已存在，请更换手机号'})
    # 以下操作为跑流程
    strs = request.strs
    data = AddPiece.piece_to_status(status, strs, product_type)
    if data in (1, 2):
        data = {"mobile": mobile}
        result_post = post(url='/v1/get/IdAndStatus', data=data)
        dict_data = json.loads(result_post)
        print('dict_data--->', dict_data),
        print('type------>', type(dict_data))
        post_data = dict_data['data'][0]
        print('post_data------->', post_data)
        print('type----------->', type(post_data))
        app_request_id = post_data['app_request_id']
        lend_request_id = post_data['lend_request_id']
        if lend_request_id == None:
            lend_request_id = 'NULL'
        current_status = post_data['current_status']
        sql = MysqlHandle.get_xml_sql(xml_path='insert_sql', xml_tag='insert', xml_id='insert_piece')
        MysqlHandle.delete_update_insert_mysql_data(
            sql.format(name=name, mobile=mobile, want_to_status=status, current_status=current_status,
                       lend_request_id=lend_request_id,
                       app_request_id=app_request_id))
        if data == 2:
            return JsonResponse({'code': 202, 'message': '已推送到个贷系统，后续状态请关注列表'})
        return JsonResponse({'code': 202, 'message': '造件已完成'})
    elif data == 3:
        return JsonResponse({'code': 202, 'message': '有异常产生，请稍后重试'})
    else:
        return JsonResponse({'code': 202, 'message': data})


@csrf_exempt
def del_product_list(request):
    product_id = request.POST['column_id']
    print('product------>', product_id)
    sql = MysqlHandle.get_xml_sql(xml_path='delete_sql', xml_tag='delete', xml_id='delete_product_list_id')
    data = MysqlHandle.delete_update_insert_mysql_data(sql=sql.format(id=product_id))
    if data:
        return HttpResponse('1')
    else:
        return HttpResponse('0')


@csrf_exempt
def del_piece_list(request):
    piece_id = request.POST['column_id']
    sql = MysqlHandle.get_xml_sql(xml_path='delete_sql', xml_tag='delete', xml_id='delete_piece_list_id')
    data = MysqlHandle.delete_update_insert_mysql_data(sql.format(id=piece_id))
    if data:
        return HttpResponse('1')
    else:
        return HttpResponse('0')


@csrf_exempt
def search_piece(request):
    app_request_id = request.GET['id']
    print(app_request_id)

    return render(request, "search-piece.html")

@csrf_exempt
def first_second_supplement(request):
    '''
    :param request:
    mobile: 手机号
    status: 判断是第一次补充材料还是第二次
    id: app进件号
    :return:
    '''
    print(request.POST)
    status = request.POST['status']
    app_request_id = request.POST['id']
    mobile = request.POST['mobile']
    if status in ('FIRST_SUPPLY_MATERIAL','SECOND_SUPPLY_MATERIAL'):

        flow = GetRequest(name='耶耶耶', mobile=mobile)
        flow.FAST_LOGIN()
        if status == 'FIRST_SUPPLY_MATERIAL':
            data = go_post('/updateManage', {'id': app_request_id})
            picture_materials_list = data['required']
            print('================',picture_materials_list)
            code = flow.picture_materials_upload(picture_materials_list)
            if code != 0:
                return JsonResponse({'code': 400, 'message': '补充照片项出现问题'}, status=400)
        # 兼容极速贷
        flow.product_type = 'TEST'
        tolend = flow.PUSH_TO_IRON()
        print('tolend-------------',tolend)
        if tolend!= 0:
            return JsonResponse({'code':400,'message':tolend},status=400)

        return JsonResponse({'code': 200, 'message': '已完成补充材料'}, status=200)






    else:
        return JsonResponse({'code': 400, 'message': '请求参数异常'}, status=400)

def a():
    time.sleep(6)
    print('---'*30,'***'*30)

@csrf_exempt
def django_test(request):
    from  django.db import connection
    connection.autocommit(False)
    cursor=connection.cursor()
    try:
        cursor.execute("update customer set name='顶顶顶顶' where id =1")
        cursor.execute("insert into  customer  VALUE (1)")
        connection.commit()
    except Exception:
        print('daafa')
        connection.rollback()

    return JsonResponse({'message':'2222222222222'})

def post(url, data):
    '''

    :param url: 链接
    :param data: 数据
    :return:
    '''
    results = requests.post(url=path.innerApiPath + url, data=json.dumps(data),
                            headers={'AUTHORIZATION': 'YLS'})
    result = results
    if result.status_code != 200:
        return 0
    return result.text


def go_post(url, data):
    request = requests.post(url=path.go_innerApiPath + url, data=data,
                            headers={'Auth': 'YLS', 'Token': 'yqaefHZs6a/wSeIO1tmd0g=='})
    if request.status_code != 200:
        return 0
    return request.json()
