import random
from datetime import date, datetime,timedelta

def getCreditCartNum(district_list):
    '''

    :param district_list: 城市编码
    :return:
    '''
    date_code = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
    date_code = str(random.randint(1950, 2005)) + date_code.strftime('%m%d') # 增加年份
    id_num = district_list + date_code + str(random.randint(100, 300))  # ，顺序号简单处理

    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                 '10': '2'}  # 校验码映射
    for i in range(0, len(id_num)):
        count = count + int(id_num[i]) * weight[i]
    idNum = id_num + checkcode[str(count % 11)]  # 算出校验码
    return idNum








if __name__ == '__main__':


    print(getCreditCartNum('130823'))