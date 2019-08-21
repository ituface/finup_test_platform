

#coding=utf-8

import time,hashlib
import json



def setparameter(dict,key,value):
    dict[key]=value


class SetHearder():
    def __init__(self):
     self.header={}

    def setHearderData(self,token=None,request_type='CUSTOMER'):
        setparameter(self.header,'Content-Type','application/json; charset=UTF-8')
        setparameter(self.header,'version','1.1')
        setparameter(self.header,'type','ANDROID')
        devicesToken=str(int(time.time()*1000))
        setparameter(self.header,'deviceToken',devicesToken)
        setparameter(self.header,'token',token)
        timestamp=str(round(int(time.time()*1000)))
        setparameter(self.header,'timestamp',timestamp)
        setparameter(self.header,'requestType',request_type)
        tokens = devicesToken if token is None else token   #如果token为空则传入devicetoken

        md5s=hashlib.md5()   #md5加密
        md5s.update(timestamp.encode('utf-8')+tokens.encode('utf-8'))
        sign=md5s.hexdigest()

        setparameter(self.header,'sign',"!signForTest")
        return self.header




if __name__=='__main__':
    hearder=SetHearder()



    import requests

    data=requests.get('http://finup-lend-app-schedule.lendapp.beta/test/pushToLend')
    print(type(data.status_code))