import traceback
import logging



class OnlineMiddlware(object):
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, *args, **kwargs):
        try:
         print('--'*30)
         respose=self.get_response(*args,**kwargs)
        except Exception as e:
            logging.error('系统报错',traceback.print_exc())
            return None
        return respose
