from CreatePiece.api.saleApi import saleApi
from CreatePiece.api.Header import SetHearder
from CreatePiece.api.AppApi import AppApi
from  public.path import path
import requests, json
import configparser
from CreatePiece.api.stauts import status
import re, time, datetime
from  CreatePiece.api.saleApi import saleApi
from public.mysql import MysqlHandle

cfg = configparser.ConfigParser()
cfg.read('./public/config.ini')

'''
生产 or 本地库
'''
host = path.Apihost


class GetRequest():
    def __init__(self, name, mobile,idNo=None,product_type='SALARY2.0_TALENT',video_check="VIDEO_SIGN",saleNo='023264',
                 salePassword='123456', year='1987'):
        '''

        :param mobile: 手机号
        :param idNo: 身份证号
        :param video_check: 签约方式
        :param name: 姓名 str
        :param status: 状态 枚举
        :param product_type: 产品枚举
        :param saleNo: 销售工号
        :param salePassword: 销售密码
        :param year 身份证年份，以判断批哪款产品

        '''
        self.name = name
        self.mobile = mobile
        self.product_type = product_type
        self.product_bool = 0
        if 'BUSINESS' in product_type:
            self.product_bool = 1
        self.saleNo = saleNo
        self.salePassword = salePassword
        self.api = AppApi
        self.code = 0
        self.year = year
        self.headers = SetHearder.setHearderData()
        self.video_check=video_check
        self.idNo=idNo

    '''
    快速登录
    '''

    def FAST_LOGIN(self):
        result = self.request_post(url=self.api.fastLogin, data=self.api.func_faselogin(self.mobile),
                                   headers=self.headers)
        if self.code:
            return result
        token = result['result'].get('token')
        self.headers = SetHearder.setHearderData(token=token)

    '''
      注册成功（包括实名，不含测一测和实名）
    '''

    def REGISTER_SUCCESS(self):
        if self.idNo==None:
            self.idNo = self.IdNo()
        if self.code:
            return self.idNo
        print('身份证号-----》', self.idNo)

        ApiList = [
            [self.api.certification, self.api.func_certification(idNo=self.idNo, salesNo=self.saleNo, name=self.name)],
            [self.api.changePassWord, self.api.func_changePassword(mobile=self.mobile)]]
        num = 1
        for inner in ApiList:
            print('num------>', num)
            data = self.request_post(url=inner[0], data=inner[1])
            num += 1
            if self.code:
                return data
        return 0

    '''
    测一测，借款请求，选择产品
    '''

    def ANSWER_PRODUCT(self):
        print('ptoduct_bool----------->', self.product_bool)
        ApiList = [[self.api.submitAnswer, self.api.func_submitAnswer(produt_bool=self.product_bool)],
                   [self.api.submitLoanApply, self.api.func_submitLoanApply()],
                   [self.api.submitProduct, self.api.func_submitProduct(self.product_type)]
                   ]
        for inner in ApiList:
            print(inner)
            data = self.request_post(url=inner[0], data=inner[1], headers=self.headers)
            if self.code:
                return data
        return 0

    '''
    基本信息
    '''

    def BASE_INFO(self):

        # 职业信息接口区分薪商
        if 'REVOLVE' in self.product_type:
            ApiList=[[self.api.fun_submitBankInfo(),self.api.submitBankInfo]]
        else:
            profession_info = self.api.postBusinessPositionInfo if self.product_bool else self.api.postPositionInfo
            isable=1
            if 'QUICK' in self.product_type:
                isable=0

            ApiList = [
                [self.api.func_postVideoCheck(self.video_check),self.api.postVideoCheck,],
                [self.api.func_submitContact(isable),self.api.sumbitContact],
                [self.api.func_submitBaseInfo(isable),self.api.submitBasicInfo],
                [ self.api.func_postBusinessPositionInfo(product_bool=self.product_bool),profession_info]
                [self.api.func_submitCutomer(),self.api.submitCutomer]
            ]
            if self.product_type=='QUICK2.0':
                ApiList.append([self.api.func_submitSupplementInfo(),self.api.submitSupplementInfo])
                ApiList.append([self.api.func_sumbitContact_v2(),self.api.sumbitContact_v2])
        for inner in ApiList:
            print(inner)
            data = self.request_post(url=inner[1], data=inner[0], headers=self.headers)
            if self.code:
                return data
        return 0

    '''
    
    拍照项
    '''

    def SubmitPicture(self):
        print('照片----------》')

        data = self.inner_post(url='/v1/get/searchProductRequired',
                               data=self.api.func_searchProductRequired(self.product_type))
        if self.code:
            return data
        self.inner_status = data['data']
        statuss = status('PhotoData')
        enum_list = list(set(self.inner_status).intersection(set(statuss)))
        if 'REVOLVE' in self.product_type:#优选计划抓取项需要enum_list
            return 0
        if self.product_type=='QUICK2.0':
            enum_list.append('INCOME_PROVE')
            enum_list.append('SOCIAL_SECURITY_FUND')
        for inner in enum_list:
            print('inner=--->', inner)
            if inner == 'ID_PHOTO':
                for i_inner in ['ID_PHOTO_reverse', 'ID_PHOTO_hand', 'ID_PHOTO_positive']:
                    datas = self.request_post(self.api.sumbitPicture, self.api.func_sumbitPicture(inner, i_inner),
                                              headers=self.headers)
            else:
                datas = self.request_post(self.api.sumbitPicture, self.api.func_sumbitPicture(applyMaterialsType=inner),
                                          headers=self.headers)
            self.request_post(url=self.api.annexstate, data=self.api.func_annexstate(inner), headers=self.headers)
            if self.code:
                return datas
        return 0

    '''
    魔蝎抓取项
    '''

    def MX_GRAB(self):

        statuss = status('GraspData')
        enum_list = list(set(self.inner_status).intersection(set(statuss)))
        if 'CREDIT_REPORT' not in enum_list:
            enum_list.append('CREDIT_REPORT')
        if len(enum_list):
            data = self.inner_post(self.api.updateMXstatus, self.api.func_updateMXstatus(self.mobile, enum_list))
            if self.code:
                return data
            return 0

        else:
            return 0

    '''
    推送到钢铁侠
    '''

    def PUSH_TO_IRON(self):
        inner_data=self.inner_post(self.api.updatefaceid,json.dumps({'mobile': self.mobile}))
        if self.code:
            return inner_data
        api = self.api.submitToSale
        api_data = self.api.func_JsonIsNull()
        data = self.request_post(url=api, data=api_data, headers=self.headers)
        if self.code:
            return data

        return 0

    '''
    推送个贷
    '''

    def PUSH_TO_LEND(self):
        saleapi = saleApi()
        data = self.inner_post(url=saleapi.deleteTokenLendRequestId,
                               data=saleapi.func_deleteTokenLendRequestId(mobile=self.mobile, sale_no=self.saleNo))
        if self.code:
            return data
        lend_request_id = data['data'].get('id')
        devices_token = str(int(time.time() * 1000))
        headers = SetHearder.setHearderData(token=None, devicesToken=devices_token, request_type='USER')
        result = self.request_post(url=saleapi.login, data=saleapi.func_login(self.saleNo, self.salePassword),
                                   headers=headers)
        if self.code:
            return result
        token = result['result'].get('token')
        print('token________>', token)
        headers = SetHearder.setHearderData(token=token, request_type='USER', devicesToken=devices_token)
        saleapi_list = [[saleapi.idNo, saleapi.func_idNo(lend_request_id)],
                        [saleapi.qualityTesting, saleapi.func_qualityTesting(lend_request_id)],
                        [saleapi.pushToLend, saleapi.func_pushToLend(lend_request_id)]]
        for inner in saleapi_list:
            inner_data = self.request_post(url=inner[0], data=inner[1], headers=headers)
            if self.code:
                return inner_data
        return 0

    '''
    生成身份证
    '''

    def IdNo(self):
        try:
            date = datetime.datetime.now().strftime('%m-%d')
            month_day = ''.join(date.split('-'))

            sql = MysqlHandle.get_xml_sql(xml_path='select_sql', xml_tag='select', xml_id='select_regions_code')
            list = MysqlHandle.select_mysql_data(sql)
            dict = list[0]
            city_code = dict['regions_code']
            print(city_code)

            key = '\d{18}|\d{17}X'
            result = requests.get(
                'http://sfz.uzuzuz.com/?region=%s&birthday=%s%s&sex=2&num=1' % (city_code, self.year, month_day)).text
            data = re.findall(key, result)
            print('data-----------》', data)
            data = ''.join(data)
            sql = MysqlHandle.get_xml_sql(xml_path='update_sql', xml_tag='update', xml_id='update_regions_enabled')
            sql = sql.format(regions_code=city_code)
            MysqlHandle.delete_update_insert_mysql_data(sql)
            print('我被调用了')
        except Exception as e:
            self.code = 1
            return '身份证id生成接口出现问题---详情请咨询小叶同学'
        return data

    '''
    app接口post请求
    '''

    def request_post(self, url, data, headers=None):
        print('url--------------->', url)
        print('host------------>',host)
        result = requests.post(url=host + url + '?sign=!signForTest', data=data.encode('utf-8'), headers=self.headers)
        get_result = result
        result_data = json.loads(get_result.text)
        code = result_data['code']
        print('接口-----%s  data----->%s' % (url, data))
        if code == '200':
            print(result_data)
            return result_data
        self.code = 1
        return '此接口-->"%s"--出现问题,message为-->"%s"--详情请看日志' % (url, result_data)

    '''
    内部接口请求post
    '''

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


# import bisect
#
# alist = ('FAST_LOGIN', 'REGISTER_SUCCESS', 'ANSWER_PRODUCT', 'BASE_INFO', 'SubmitPicture', 'MX_GRAB', 'PUSH_TO_IRON',
#          'PUSH_TO_LEND')
#
# gtr=eval("GetRequest(name='跑一遍',mobile='18908477022',product_type='BUSINESS2.0_CAR')")
# #gtr = GetRequest(name='魔蝎抓取', mobile='18908433092')
#
#
# for i in alist[-4:]:
#     print('步骤----》',i)
#     s=eval('gtr.%s()'%i)
#     print(s)
