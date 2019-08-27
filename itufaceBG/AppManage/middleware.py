import traceback
import logging

from django.shortcuts import HttpResponse

# class OnlineMiddlware(object):
#     def __init__(self,get_response):
#         self.get_response=get_response
#
#     def __call__(self, *args, **kwargs):
#         try:
#          respose=self.get_response(*args, **kwargs)
#         except Exception as e:
#             print('系统报错')
#             return HttpResponse('fffff')
#         return respose



class ExceptionTestMiddleware(object):
    # 如果注册多个process_exception函数，那么函数的执行顺序与注册的顺序相反。(其他中间件函数与注册顺序一致)
    # 中间件函数，用到哪个就写哪个，不需要写所有的中间件函数。
    def process_exception(self, request, exception):
        '''视图函数发生异常时调用'''
        print('----process_exception1----')
        print(exception)
