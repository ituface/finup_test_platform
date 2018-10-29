import xml.etree.ElementTree as ET
import configparser
import pymysql
cfg=configparser.ConfigParser()
cfg.read('./public/config.ini')


'''
生产 or 本地库
'''
huanjing='mysql_test'
#huanjing='mysql_sc'



host = cfg.get(huanjing,'host')
port=cfg.get(huanjing,'port')
user=cfg.get(huanjing,'user')
passwd=cfg.get(huanjing,'passwd')
db=cfg.get(huanjing,'db')



class MysqlHandle:
    conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset='utf8')
    conn.ping(reconnect=True)


    '''
    查询数据
    '''
    @classmethod
    def select_mysql_data(cls, sql):

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
    def delete_update_insert_mysql_data(cls,sql):
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
        tree = ET.parse('./xml/%s' % xml_path)
        root = tree.getroot()
        select = root.findall(xml_tag)
        return ''.join([i.text for i in select if i.get("id") == xml_id]).strip()
