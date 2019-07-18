import json, time, base64


class AppApi():
    '''
    app api
    '''
    fastLogin = '/home/v1/fastLogin'  # 快速登录
    certification = '/apply/v1/certification'  # 实名认证
    changePassWord = '/home/v1/changePassWord'  # 修改密码
    submitAnswer = '/apply/v1/submitAnswer'  # 保存测一测密码
    submitLoanApply = '/apply/v1/submitLoanApply'  # 提交借款申请
    submitProduct = '/apply/v1/submitProduct'  # 选择产品
    sumbitContact = '/contact/v1/submit'  # 提交联系人信息
    submitBasicInfo = '/basic/v2/submitBasicInfo'  # 提交基本信息
    postVideoCheck = '/video/v1/postVideoCheck'  # 提交签约方式
    postBusinessPositionInfo = '/position/v1/postBusinessPositionInfo'  # 提交职业信息 商
    postPositionInfo = '/position/v1/postPositionInfo'  # 薪类
    sumbitPicture = '/annex/v1/upload/picture'  # 提交拍照像
    annexstate = '/annex/v1/change/state'  # 更新拍照项状态
    submitToSale = '/apply/v1/submitToSale'  # 提交钢铁侠
    submitCutomer = '/basic/v1/submit/customer/id'  # 提交客户身份证信息
    timestamp = int(time.time() * 1000)

    # 补充一提交资料
    submitSupplementInfo = '/basic/v1/submitSupplementInfo'
    sumbitContact_v2 = '/contact/v3/submit'

    # 优选计划提交银行卡接口
    submitBankInfo = '/bank/v1/submitBankInfo'

    # 内部接口
    searchProductRequired = '/v1/get/searchProductRequired'
    SearchResult = '/v1/get/SearchResult'
    updateMXstatus = '/v1/get/updateMXstatus'  # 更新魔蝎状态
    updatefaceid = '/v1/set/updatefaceid'  # 跳过人脸

    IdAndStatus = '/v1/get/IdAndStatus'  # 获取当前手机所对应的app 进件号和状态

    '''
    快速登录
    '''

    @staticmethod
    def func_faselogin(mobile):
        data = {"mobile": "%s" % mobile, "idfa": "1", "verificationCode": "%s" % '000000',
                "alias": "1"}
        return json.dumps(data)

    '''
    实名认证json
    '''

    @staticmethod
    def func_certification(idNo, name, salesNo='023264'):
        '''
        :param idNo: str
        :param name: str
        :param salesNo: str
        :return: json
        '''
        data = {"idNo": idNo, "salesNo": salesNo, "shopCode": "RPA2450101", "shopId": 103,
                "shopName": "南宁民族大道门店", "userName": name}
        return json.dumps(data)

    '''
    修改密码
    '''

    @staticmethod
    def func_changePassword(mobile):
        '''

        :param mobile: str
        :return: json
        '''

        data = {"mobile": mobile, "newPassword": "a12345678", "verificationCode": "000000"}
        return json.dumps(data)

    '''
    保存测一测答案
    '''

    @staticmethod
    def func_submitAnswer(produt_bool=0):
        '''

        :param produt_type: bool  0 薪 1商
        :return: json
        '''
        data = {"answer": "1"}
        if int(produt_bool):
            data['answer'] = '2'
        return json.dumps(data)

    '''
    借款申请
    '''

    @staticmethod
    def func_submitLoanApply():
        data = {"loanAmount": 100000, "loanPurposeType": "EDUCATION_TRAINING"}
        return json.dumps(data)

    '''
    选择产品
    '''

    @staticmethod
    def func_submitProduct(product_name):
        '''

        :param product_type: str
        :return: json
        '''
        data = {"productType": product_name, "tongdunToken": "tongduntoken"}
        return json.dumps(data)

    '''
    联系人信息
    '''

    @staticmethod
    def func_submitContact(isable=1):

        if isable:
            AppApi.sumbitContact = '/contact/v4/submit'
            data = {
                "contactVoList": [{
                    "contactMobile": "13546696666",
                    "contactName": "付上",
                    "department": "",
                    "isKnow": 0,
                    "relation": "FATHER",
                    "relationExplain": "",
                    "relationType": "LINEAL_RELATIVES"
                }, {
                    "contactMobile": "13549949966",
                    "contactName": "母上",
                    "department": "",
                    "isKnow": 0,
                    "relation": "MOTHER",
                    "relationExplain": "",
                    "relationType": "LINEAL_RELATIVES"
                }, {
                    "contactMobile": "13579966333",
                    "contactName": "王大猪",
                    "department": "销售部",
                    "isKnow": 0,
                    "relation": "COLLEAGUE",
                    "relationExplain": "",
                    "relationType": "WORK_CERTIFICATE"
                }],
                "startTime": AppApi.timestamp
            }
        else:
            AppApi.sumbitContact = '/contact/v3/submit'

            data = {
                "contactVoList": [{
                    "contactMobile": "13569996666",
                    "contactName": "父上大人",
                    "department": "",
                    "isKnow": 1,
                    "relation": "FATHER",
                    "relationExplain": "",
                    "relationType": "LINEAL_RELATIVES"
                }]
            }
        return json.dumps(data)

    '''
    提交签约方式
    '''

    @staticmethod
    def func_postVideoCheck(video_check):
        data = {
            "videoCheck": video_check  # VIDEO_SIGN  OFF_SIGN
        }
        print('video--------》', data)
        return json.dumps(data)

    '''
    基本信息
    '''

    @staticmethod
    def func_submitBaseInfo(isable=1):
        if isable:
            AppApi.submitBasicInfo = '/basic/v2/submitBasicInfo'

            data = {"annualIncome": "1000000", "bankNo": "6221501000003361474", "carPropertyType": "HAVE_CAR_AND_LOAN",
                    "childrenNumber": 0.0, "city": "北京", "cityCode": "110100", "dist": "东城区", "distCode": "110101",
                    "education": "UNDERGRADUATE", "email": '%s@163.com' % str(int(time.time() * 1000)),
                    "housePropertyType": "NO_HOUSE", "lifeYears": 20.0,
                    "livingType": "SELF_HOUSE", "livingTypeOther": "asdf", "marriage": "UNMARRIED",
                    "mobile1": "18618430076", "province": "北京市", "provinceCode": "110000", "qq": 174323928,
                    "town": "朝阳区物资学院", "repaySource": "WAGE_INCOME"}  # 还款来源：repaySource
        else:
            AppApi.submitBasicInfo = '/basic/v3/submitBasicInfo'
            data = {
                "city": "市辖区",
                "marriage": "UNMARRIED",
                "email": "%s@163.com" % str(int(time.time() * 1000)),
                "idCardProvince": "北京市",
                "province": "北京市",
                "idCardCityCode": "110100",
                "idCardTown": "您虹魔",
                "dist": "东城区",
                "distCode": "110101",
                "cityCode": "110100",
                "annualIncome": "666",
                "idCardDistCode": "110101",
                "town": "还比查查",
                "housePropertyType": "NO_HOUSE",
                "idCardDist": "东城区",
                "provinceCode": "110000",
                "idCardProvinceCode": "110000",
                "education": "SEN",
                "idCardCity": "市辖区",
                "carPropertyType": "NO_CAR",
                "bankNo": "6227000014970288456"
            }
        return json.dumps(data)

    '''
    职业信息
    '''

    @staticmethod
    def func_postBusinessPositionInfo(product_bool=0):
        '''

        :param product_bool: bool  0薪 1商
        :return: json
        '''
        if product_bool == 0:
            data = {
                "positionExplain": "",
                "companyAttributeDesc": "机关事务单位",
                "positionName": "GENERAL_STAFF",
                "city": "市辖区",
                "province": "北京市",
                "attributeExplain": "",
                "dist": "东城区",
                "officialJobTime": 1467302400000,
                "distCode": "110101",
                "cityCode": "110100",
                "positionNameDesc": "正式员工",
                "accumulationFund": "0",
                "town": "民工",
                "companyName": "您虹魔",
                "specialUnitType": "GOVERNMENT_INSTITUTIONS",
                "telephone": "011-6498555-6",
                "provinceCode": "110000",
                "entryTime": 1498838400000,
                "companyAttribute": "ENTERPRISE_COMPANY",
                "salaryGetForm": "SALARY_BANK_CARD",
                "specialOccupationType": "ACCOUNTANT",
                "department": "名模"
            }
        else:
            data = {
                "distCode": "110101",
                "specialUnitType": "GOVERNMENT_INSTITUTIONS",
                "province": "北京市",
                "town": "陌陌",
                "city": "市辖区",
                "provinceCode": "110000",
                "cityCode": "110100",
                "companyName": "凡普金科卡卡卡",
                "dist": "东城区",
                "telephone": "011-6490662-3",
                "officialJobTime": "1498838400000"
            }
        return json.dumps(data)

    '''
    提交拍照像
    '''

    @staticmethod
    def func_sumbitPicture(applyMaterialsType, fileName=0):
        '''

        :param applyMaterialsType: enum
        :param fileName: str
        :return: json
        '''
        f = open("./static/images/image.jpg", 'rb').read()
        image = str(base64.b64encode(f), encoding='utf-8')
        if fileName == 0:
            fileName = AppApi.timestamp
        data = {"uploadType": "LINE_UPPER", "applyMaterialsType": applyMaterialsType,
                "fileList": [{"fileName": fileName, "fileStream": image}]}
        return json.dumps(data)

    '''
    更新拍照项状态
    '''

    @staticmethod
    def func_annexstate(applyMaterialsType):
        '''

        :param applyMaterialsType: enum
        :return: json
        '''
        data = {"uploadType": "LINE_UPPER", "applyMaterialsType": applyMaterialsType}
        return json.dumps(data)

    '''
    json为{}
    '''

    @staticmethod
    def func_JsonIsNull():
        return json.dumps({})

    '''
    
    每个产品必填项
    '''

    @staticmethod
    def func_searchProductRequired(product_name):
        return json.dumps({'product_name': product_name})

    '''搜索数据库中符合的进件'''

    @staticmethod
    def func_SearchResult(product_name):
        return json.dumps({'status': product_name})

    @staticmethod
    def func_updateMXstatus(mobile, type):
        '''

        :param mobile: 手机号
        :param type: 要更改的魔蝎状态 list
        :return:
        '''
        return json.dumps({'mobile': mobile, 'type': type})

    @staticmethod
    def func_submitCutomer():
        return json.dumps({
            "cityCode": "110100",
            "provinceCode": "110000",
            "city": "市辖区",
            "dist": "西城区",
            "town": "街道",
            "validTermStart": "2015-03-29",
            "validTermFinish": "2019-03-29",
            "houseCity": "false",
            "distCode": "110102",
            "province": "北京市"
        })

    @staticmethod
    def fun_submitBankInfo():
        return json.dumps({
            "cardNo": "%s" % int(time.time() * 1000)
        })

    def __del__(self):

        print('我被销毁了。。。。。啦啦啦啦啦啦啦啊')
