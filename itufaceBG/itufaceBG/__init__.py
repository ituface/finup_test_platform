import pymysql
from itufaceBG.CreatePiece.SqlCron import update_city_code
from itufaceBG.CreatePiece.SqlCron import insert_statistics_amount
pymysql.install_as_MySQLdb()


print('==========ssss==============')
update_city_code()
insert_statistics_amount()