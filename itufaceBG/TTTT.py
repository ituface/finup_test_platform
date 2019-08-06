import requests

def go_post(url,data):
    request=requests.post(url='http://127.0.0.1:8882'+url,data=data,headers={'Auth':'YLS','Token':'yqaefHZs6a/wSeIO1tmd0g=='})
    if request.status_code!=200:
        return  0
    return request.json()



if __name__ == '__main__':

   b=go_post('/updateManage',{'id':'10003033'})
   print(type(b))