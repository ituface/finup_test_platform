import traceback
import logging

from django.shortcuts import HttpResponse

class OnlineMiddlware(object):
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, *args, **kwargs):

        respose=self.get_response(*args, **kwargs)
        return respose

    def process_exception(self, request, exception):
        traceback.print_exc()
        return HttpResponse('有异常产生，稍后重试')


