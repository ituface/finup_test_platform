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
    timestamp = int(time.time() * 1000)

    # 内部接口
    searchProductRequired = '/v1/get/searchProductRequired'
    SearchResult = '/v1/get/SearchResult'
    updateMXstatus = '/v1/get/updateMXstatus'  # 更新魔蝎状态

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
        data = {"answer": "12"}
        if int(produt_bool):
            data['answer'] = '212'
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
            data = {
                "contactVoList": [
                    {"contactMobile": "18220022211", "contactName": "王朗", "department": "信息科", "isKnow": "0",
                     "relation": "FATHER", "relationExplain": "string", "relationType": "LINEAL_RELATIVES"},
                    {"contactMobile": "13577772222", "contactName": "王明阳", "department": "信息科", "isKnow": "0",
                     "relation": "MOTHER", "relationExplain": "string", "relationType": "LINEAL_RELATIVES"},
                    {"contactMobile": "17308882222", "contactName": "叶利钦", "department": "信息科",
                     "isKnow": "0",
                     "relation": "RELATIVES", "relationExplain": "string",
                     "relationType": "WORK_CERTIFICATE"},
                    {"contactMobile": "16722233322", "contactName": "斯大林", "department": "信息科", "isKnow": "0",
                     "relation": "COLLEAGUE", "relationExplain": "string", "relationType": "OTHER_CONTACTS"}],
                "startTime": AppApi.timestamp}
        else:
            AppApi.sumbitContact = '/contact/v2/submit'
            data = {
                "contactVoList": [{
                    "contactMobile": "13662669333",
                    "contactName": "母亲大人",
                    "department": "",
                    "isKnow": 1,
                    "relation": "MOTHER",
                    "relationExplain": "",
                    "relationType": "LINEAL_RELATIVES"
                }, {
                    "contactMobile": "17600810361",
                    "contactName": "同事二蛋",
                    "department": "",
                    "isKnow": 0,
                    "relation": "COLLEAGUE",
                    "relationExplain": "",
                    "relationType": "OTHER_CONTACTS"
                }]
            }
        return json.dumps(data)

    '''
    提交签约方式
    '''

    @staticmethod
    def func_postVideoCheck(video_check):
        data = {
            "videoCheck":video_check   #VIDEO_SIGN  OFF_SIGN
        }
        print('video--------》',data)
        return json.dumps(data)

    '''
    基本信息
    '''

    @staticmethod
    def func_submitBaseInfo(isable=1):
        if isable:
            AppApi.submitBasicInfo = '/basic/v2/submitBasicInfo'

            data = {"annualIncome": "1000000", "bankNo": "77722223333322", "carPropertyType": "HAVE_CAR_AND_LOAN",
                    "childrenNumber": 0.0, "city": "北京", "cityCode": "110100", "dist": "东城区", "distCode": "110101",
                    "education": "UNDERGRADUATE", "email": '%s@163.com' % str(int(time.time() * 1000)),
                    "housePropertyType": "NO_HOUSE", "lifeYears": 20.0,
                    "livingType": "SELF_HOUSE", "livingTypeOther": "asdf", "marriage": "UNMARRIED",
                    "mobile1": "18618430076", "province": "北京市", "provinceCode": "110000", "qq": 174323928,
                    "town": "朝阳区物资学院", "repaySource": "WAGE_INCOME"}   #还款来源：repaySource
        else:
            AppApi.submitBasicInfo = '/basic/v3/submitBasicInfo'
            data = {
                "city": "市辖区",
                "email": '%s@163.com' % str(int(time.time() * 1000)),
                "marriage": "UNMARRIED",
                "province": "北京市",
                "dist": "东城区",
                "distCode": "110101",
                "cityCode": "110100",
                "annualIncome": "3663.00",
                "town": "银河护卫队A座凡普金科集团有限公司亚龙湾",
                "housePropertyType": "HAVE_HOUSE_AND_LOAN_WITHOUT",
                "provinceCode": "110000",
                "livingType": "HOME_HOUSE",
                "education": "SEN",
                "livingTypeOther": "",
                "bankNo": "623166446666"
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
                "distCode": "110101",
                "officialJobTime": 1475251200000,
                "cityCode": "110100",
                "positionNameDesc": "正式员工",
                "accumulationFund": "0",
                "town": "详细地址北京",
                "companyName": "现单位名称",
                "telephone": "011-6490662-0",
                "provinceCode": "110000",
                "entryTime": 1543593600000,
                "companyAttribute": "ENTERPRISE_COMPANY",
                "salaryGetForm": "SALARY_BANK_CARD",
                "department": "现单位部门"
            }
        else:
            data = {"town": "健健康康健健康康", "companyName": "来猜猜吧", "telephone": "011-1111111-11", "city": "北京市",
                    "provinceCode": "110102", "province": "西城区", "dist": "市辖区", "officialJobTime": "1535731200000",
                    "distCode": "110100", "cityCode": "110000"}
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
