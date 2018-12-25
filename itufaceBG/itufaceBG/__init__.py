import pymysql
from CreatePiece.SqlCron import update_city_code

pymysql.install_as_MySQLdb()


print('==========ssss==============')
update_city_code()