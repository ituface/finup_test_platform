import traceback
import logging

from django.shortcuts import HttpResponse

class OnlineMiddlware(object):
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, *args, **kwargs):
        try:
         print('--'*30,self.get_response.__name__)

         respose=self.get_response(*args, **kwargs)
        except ValueError as e:
            print('系统报错')
            return HttpResponse('fffff')
        return respose


