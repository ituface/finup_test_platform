import requests
from CreatePiece.api.stauts import status
from public.path import path
import json
from CreatePiece.api.GetRequest import GetRequest
import bisect


class AddPiece():
    @staticmethod
    def mobile_enable(mobile):

        data = {'mobile': mobile}
        data = AddPiece.inner_post(url='/v1/get/mobileEnable', data=json.dumps(data))
        if int(data['data']):
            return 1
        else:
            return 0

    @staticmethod
    def piece_to_status(request_status, eval_strs):
        try:
            app_status = status('lend_app')
            lend_status = status('lend')
            position = app_status.index(request_status) + 1
            print('position---------------》', position)
            gtr = eval('GetRequest(%s)' % eval_strs)
            if request_status in app_status:
                for inner_status in range(position):
                    data = eval("gtr.%s()" % app_status[inner_status])
                    print('inner-----<', inner_status)
                    if data:
                        return data
                return 1
            if request_status in lend_status:
                for inner_lend_status in app_status:
                    data = eval('gtr.%s()' % inner_lend_status)
                    if data:
                        return data
                return 2

        except ValueError as e:
            return 3

    @classmethod
    def inner_post(self, url, data):
        try:
            data = requests.post(url=path.innerApiPath + url, data=data.encode('utf-8'),
                                 headers={'AUTHORIZATION': 'YLS'})
            result = data
            if result.status_code != 200:
                self.code = 1
                return '此接口-->"%s"--出现问题--详情请问小叶同学' % url
        except Exception as e:
            self.code = 1
            return e
        return json.loads(result.text)
