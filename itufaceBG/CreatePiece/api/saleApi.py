import json


class saleApi():
    '''
    钢铁侠api
    '''

    qualityTesting = '/saleLoan/v1/automatic/qualityTesting'  # 一键质检
    pushToLend = '/saleLoan/v1/pushToLend'  # 推送个贷
    login = '/saleLogin/v1/login'  # 登录
    idNo = '/saleLoan/v1/submit/customer/id'

    '''
    内部接口
    '''
    deleteTokenLendRequestId = '/v1/get/deleteTokenLendRequestId'  # 删除销售token ，返回用户app_lend_request_id

    '''
       登录
       '''

    @staticmethod
    def func_login(salesNo='023264', salepassword='123456'):
        '''

        :param salesNo: str
        :param password: str
        :return:
        '''
        data = {
            "password": salepassword,
            "salesNo": salesNo
        }
        return json.dumps(data)

    '''
    一键质检
    '''

    @staticmethod
    def func_qualityTesting(appLendRequestId):
        '''
        :param appLendRequestId: int
        :return: json
        '''

        data = {
            "appLendRequestId": int(appLendRequestId),
            "createTime": "2018-11-13T02:31:27.312Z",
            "materialName": "string",
            "materialType": "string",
            "startTime": "2018-11-13T02:31:27.312Z",
            "status": "未填写",
            "updateTime": "2018-11-13T02:31:27.312Z"
        }
        return json.dumps(data)

    '''
    推送个贷
    '''

    @staticmethod
    def func_pushToLend(appLendRequestId):
        '''
        :param appLendRequestId: int
        :return: json
        '''
        data = {
            "appLendRequestId": appLendRequestId,
            "tongdunToken": "string"
        }
        return json.dumps(data)

    @staticmethod
    def func_deleteTokenLendRequestId(mobile, sale_no):
        '''
        :param mobile: 手机号
        :param sale_no: 销售号
        :return:
        '''
        return json.dumps({"sale_no": sale_no, "mobile": mobile})

    @staticmethod
    def func_idNo(appLendRequestId):
        data = {
            "validTermStart": "2008-12-14",
            "town": "街道小区楼",
            "houseNumber": "门牌号",
            "appLendRequestId": appLendRequestId,
            "provinceCode": "110000",
            "city": "市辖区",
            "validTermFinish": "2023-12-14",
            "province": "北京市",
            "dist": "东城区",
            "distCode": "110101",
            "cityCode": "110100",
            "houseCity": False
        }

        return json.dumps(data)
