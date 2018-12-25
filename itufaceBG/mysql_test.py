import xml.etree.ElementTree as ET
import configparser
import pymysql
from public.path import path

cfg = configparser.ConfigParser()
cfg.read('../public/config.ini')
import datetime

'''
生产 or 本地库
'''

host = path.host
port = path.port
user = path.user
passwd = path.passwd
db = path.db


class MysqlHandle:
    conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset='utf8')
    conn.ping(reconnect=True)

    '''
    查询数据
    '''

    @classmethod
    def select_mysql_data(cls, sql):
        try:
            cls.conn.ping()
        except:
            cls.conn()

        cursor = cls.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchall();
            cls.conn.commit()
        except TypeError as e:
            print(e)
            data = []
        cursor.close()
        return data

    @classmethod
    def delete_update_insert_mysql_data(cls, sql):
        try:
            cls.conn.ping()
        except:
            cls.conn()
        cursor = cls.conn.cursor()
        tag = cursor.execute(sql)
        cls.conn.commit()
        cursor.close()
        cls.conn.close()
        return tag

    @classmethod
    def reConnect(cls):
        try:
            cls.conn.ping()
        except:
            cls.conn()

    @classmethod
    def get_xml_sql(cls, xml_path, xml_tag, xml_id):
        tree = ET.parse("./xml/%s" % xml_path)
        root = tree.getroot()
        select = root.findall(xml_tag)
        return ''.join([i.text for i in select if i.get("id") == xml_id]).strip()


def workday_to_date():
    date_list = []
    today = datetime.datetime.now()
    for i in range(1, 8):
        offset = datetime.timedelta(days=-i)
        re_date = (today + offset).strftime('%Y-%m-%d')
        re_dates = datetime.datetime.strptime('%s' % re_date, '%Y-%m-%d').weekday()
        if re_dates in (5, 6):
            continue
        date_list.append('%s' % re_date)
    return date_list



def insert_statistics_amount():
    # 计算昨天日期
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-1)
    yesterday = (today + offset).strftime('%Y-%m-%d')
    # 查询昨日造件数量
    piece_sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_chart_piece')
    piece_data = MysqlHandle.select_mysql_data(piece_sql.format(create_time=yesterday))
    piece_number = piece_data[0].get('number')
    # 查询昨日上传包数量
    app_sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_chart_app')
    app_data = MysqlHandle.select_mysql_data(app_sql.format(create_time=yesterday))
    app_number = app_data[0].get('number')

    # 将数量插入到statistics_amount中
    statistics_tuple = ((piece_number, 'PIECE'), (app_number, 'APP'))
    statistics_sql = MysqlHandle.get_xml_sql(xml_path='insert_sql', xml_tag='insert',
                                             xml_id='insert_into_statistics_data')
    for inner in statistics_tuple:
       tag= MysqlHandle.delete_update_insert_mysql_data(
            statistics_sql.format(date_record=yesterday, count=inner[0], category=inner[1]))
       print('tag----->',tag)



date=[]
count=[]
sql=MysqlHandle.get_xml_sql(xml_path='select_sql',xml_tag='select',xml_id='select_statistics_amount_app_data')
data=MysqlHandle.select_mysql_data(sql)
for i in data:
    inner='%d'%i['date']
    date.append(int(i['date']))
    count.append(i['count'])
print(date)
print(count)
