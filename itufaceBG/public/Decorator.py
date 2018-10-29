from django.shortcuts import redirect, render
from django.http import QueryDict
import xml.etree.ElementTree as ET

tree = ET.parse('./xml/select_sql')
root = tree.getroot()
select = root.findall('select')
getXmlSql = lambda a: ''.join([i.text for i in select if i.get("id") == a]).strip()


# 当cookie过期后回到登录界面
def Check_login(func):
    def inner(request, *args, **kwargs):
        if request.COOKIES.get('username') == None:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return inner


# 时间操作

def Handle_time(func):
    def inner(request, *args, **kwargs):
        if request.method == 'POST':
            dicts = dict(request.POST)
            start=dicts.get('create_time')
            end=dicts.get('end_time')
            str_data = ''
            if len(start) and  len(end)== 0:
                return func(request, *args, **kwargs)
            if start[0] != '':
                str_data = str_data + ' and create_time>"%s"' % start[0]
            if end[0]!= '':
                str_data = str_data + ' and create_time<"%s"' % end[0]
            datas = request.DPOST.get('sql')
            print('datas======>',datas)
            sql = datas + str_data
            request.DPOST = QueryDict('sql=%s' % sql)
        return func(request, *args, **kwargs)

    return inner


# 通过SqlStatement解析xml 获取sql语句，然后通过request.POST传回
def get_web_input_data(SqlStatement):
    def outer(func):
        def inner(request, *args, **kwargs):
            sql = getXmlSql(SqlStatement)  # 获取sql语句
            if request.method == 'POST':
                accept_data = dict(request.POST)
                for i in list(accept_data.keys()):
                    if ''.join(accept_data[i]) == '':
                        del accept_data[i]
                sql_data = []
                sql_data.append(sql)
                sql_data.append('where 1=1')
                # 通过for循环把前端传过来的判断添加到sql里
                print('accept_data---->',accept_data)
                for key in accept_data.keys():
                    if key in ('create_time' , 'end_time') :
                        continue
                    sql_data.append('and')
                    sql_data.append(key)
                    sql_data.append('=')
                    sql_data.append("'%s'" % ''.join(accept_data[key]))
                sql = ' '.join(sql_data)

            request.DPOST = QueryDict('sql=%s' % sql)
            return func(request, *args, **kwargs)

        return inner

    return outer
