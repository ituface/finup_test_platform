
#上线要改
class path():
    Apihost='http://finup-lend-app-server.lendapp.beta'
    innerApiPath='http://10.10.180.206:8088'
    #测试地址
   # innerApiPath='http://127.0.0.1:8088'
    #测试地址
    # host = '127.0.0.1'
    # port = 3306
    # user = 'root'
    # passwd = 'root123'
    # db = 'yyy'
    #线上地址
    host='10.10.180.206'
    port=3306
    user = 'root'
    passwd = 'root123!@YE'
    db = 'lend_app'

    s='app'
    #外部调用地址
    ToChangeStatus='http://10.10.180.206:8090/updateLendApp'


