import traceback
import logging
from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import HttpResponse

class OnlineMiddlware(object):
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request, *args, **kwargs):
        try:
         print('--'*30)
         respose=self.get_response(request, *args, **kwargs)
        except Exception as e:
            print('系统报错', traceback.print_exc())
            logging.error('系统报错',traceback.print_exc())
            return
        return respose


