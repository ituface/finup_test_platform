import traceback
import logging

from django.shortcuts import HttpResponse

class OnlineMiddlware(object):
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, *args, **kwargs):
        try:
         respose=self.get_response(*args, **kwargs)
        except Exception as e:
            print('系统报错')
            return HttpResponse('fffff')
        return respose


