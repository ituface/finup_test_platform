import requests
from CreatePiece.api.stauts import status
from public.path import path
import json
from CreatePiece.api.GetRequest import GetRequest
import bisect
import traceback


class AddPiece():
    @staticmethod
    def mobile_enable(mobile):

        data = {'mobile': mobile}
        data = AddPiece.inner_post(url='/v1/get/mobileEnable', data=json.dumps(data))
        print('data----------------',data)
        if int(data['data']):
            return 1
        else:
            return 0

    @staticmethod
    def piece_to_status(request_status, eval_strs,product_type=None):
        '''

        :param request_status: 所要到的状态
        :param eval_strs: 造件信息传递
        :param product_type: 为了区分老友计划和优选计划
        :return:
        '''
        try:
            if 'EXTENSION' in product_type :
                app_status = status('old_friend_plan')
                if request_status not in app_status:
                    position=len(app_status)
                else:
                    position=app_status.index(request_status) + 1
            elif 'REVOLVE' in product_type:
                app_status = status('Optimal_plan')
                if request_status not in app_status:
                    position = len(app_status)
                else:
                    position = app_status.index(request_status) + 1
            else:
                app_status = status('lend_app')
                position = app_status.index(request_status) + 1
            lend_status = status('lend')
            print('参数-------------------------------------------------------》',product_type)
            gtr = eval('GetRequest(%s)' % eval_strs)

            if request_status in app_status or 'EXTENSION' in product_type or 'REVOLVE' in product_type:
                for inner_status in range(position):
                    data = eval("gtr.%s()" % app_status[inner_status])
                    print('inner-----<', inner_status)
                    if data:
                        return data

                if  'EXTENSION' in product_type  or 'REVOLVE' in product_type:
                    headers = {
                        'Connection': 'close',
                    }
                    data=requests.get('http://finup-lend-app-schedule.lendapp.beta/test/pushToLend',headers=headers)
                    if data.status_code!=200:
                        return '定时器接口出现问题。。请手动触发'
                return 1
            if request_status in lend_status:
                for inner_lend_status in app_status:
                    data = eval('gtr.%s()' % inner_lend_status)
                    del gtr
                    if data:
                        return data
                return 2

        except Exception as e:
            print(traceback.print_exc())
            return 3

    @classmethod
    def inner_post(self, url, data):
        try:
            data = requests.post(url=path.innerApiPath + url, data=data.encode('utf-8'),
                                 headers={'AUTHORIZATION': 'YLS'})
            print(path.innerApiPath + url)
            result = data

            print('result--------------------',data)
            if result.status_code != 200:
                self.code = 1
                return '此接口-->"%s"--出现问题--详情请问小叶同学' % url
        except Exception as e:
            self.code = 1
            return e
        return json.loads(result.text)
