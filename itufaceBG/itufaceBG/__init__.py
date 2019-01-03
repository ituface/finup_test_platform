import pymysql
from CreatePiece.SqlCron import update_city_code
from CreatePiece.SqlCron import insert_statistics_amount
from CreatePiece.SqlCron import task
pymysql.install_as_MySQLdb()


print('==========ssss==============')
update_city_code()
insert_statistics_amount()
task()