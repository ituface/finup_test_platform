# import datetime
# # today = datetime.datetime.now()
# # tadss= datetime.datetime.now().strftime('%Y-%m-%d')
# # print(tadss)
# # offset = datetime.timedelta(days=-3)
# # re_date = (today + offset).strftime('%Y-%m-%d')
# # print(re_date.weekday())
# #
# #
# #
# # today_week=datetime.datetime.now().weekday()
# # print(today_week)
#
#
#
# # print(datetime.datetime.strftime('20181218','%Y%m%d').weekday())
#
#
# import datetime
#
# today=datetime.datetime.now()
# offset=datetime.timedelta(days=-4)
# re_date = (today + offset).strftime('%Y-%m-%d')
# print(re_date)
# re_dates=datetime.datetime.strptime('%s'%re_date,'%Y-%m-%d').weekday()
# print(re_dates)
#
#
# def workday_to_date():
#     date_list=[]
#     today=datetime.datetime.now()
#     for i in range(1,8):
#         offset = datetime.timedelta(days=-i)
#         re_date = (today + offset).strftime('%Y-%m-%d')
#         re_dates = datetime.datetime.strptime('%s' % re_date, '%Y-%m-%d').weekday()
#         if re_dates in(5,6):
#             continue
#         date_list.append('%s'%re_date)
#     return date_list
#
# print(workday_to_date())
#
#
# date=['2018-12-20', '2018-12-19', '2018-12-18', '2018-12-17', '2018-12-14']
# date_dao=date[::-1]
# print(date_dao)
#
# source=[{'number': 8, 'date': '2018-12-13'}, {'number': 11, 'date': '2018-12-14'}, {'number': 9, 'date': '2018-12-17'}, {'number': 5, 'date': '2018-12-18'}, {'number': 11, 'date': '2018-12-19'}]
# for inner in source:
#     print(inner['date'])
# class A():
#     def __init__(self,name):
#
#         self.name=name
#     def  bu(self):
#         return 3
#
#     def __getattribute__(self, item):
#         try:
#             super(A,self).__getattribute__(item)
#         except KeyError:
#             return 'default'
#
# a=A('ui')
# print(a.name)
# print(a.bs)
# print(a.__dict__)
# print(hasattr(a,'909090'))


import  requests


code=requests.post(url='http://10.10.180.206:8090/updateLendApp',data={'mobile':'17800038282','state_type':'SALE_EXAMINE'})
print(code.text)