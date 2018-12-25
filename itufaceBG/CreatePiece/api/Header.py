

#coding=utf-8

import time,hashlib
import json



def setparameter(dict,key,value):
    dict[key]=value


class SetHearder():
    header={}

    @classmethod
    def setHearderData(cls,token=None,devicesToken='720E0E48-FFC1-4D3F-A750-861FFA2726F5',request_type='CUSTOMER'):
        setparameter(cls.header,'Content-Type','application/json; charset=UTF-8')
        setparameter(cls.header,'version','1.1')
        setparameter(cls.header,'type','ANDROID')
        setparameter(cls.header,'deviceToken',devicesToken)
        setparameter(cls.header,'token',token)
        timestamp=str(round(int(time.time()*1000)))
        setparameter(cls.header,'timestamp',timestamp)
        setparameter(cls.header,'requestType',request_type)
        tokens = devicesToken if token is None else token   #如果token为空则传入devicetoken

        md5s=hashlib.md5()   #md5加密
        md5s.update(timestamp.encode('utf-8')+tokens.encode('utf-8'))
        sign=md5s.hexdigest()

        setparameter(cls.header,'sign',"!signForTest")
        return cls.header




if __name__=='__main__':
    hearder=SetHearder()
    print(hearder.setHearderData()[1])

