from django.test import TestCase


from django.http import HttpRequest
from CreatePiece.views import add_piece_api,django_test


class AddPieceApiTest(TestCase):


    def test_add_piece_api_post_request(self):
        request=HttpRequest()
        request.method='POST'
        request.POST['name']='测试一'
        request.POST['mobile']='19429008018'
        request.POST['status']='PUSH_TO_IRON'
        request.POST['num']='1'
        request.POST['product_type']=''
        request.POST['saleNo']=''
        request.POST['salePassword']=''
        request.POST['year']=''
        request.POST['video_check']='OFF_SIGN'
        request.POST['idNo']=''

        response=add_piece_api(request)
        result=response.content.decode()
        china_code=result.encode('utf-8').decode('unicode-escape')
        print(china_code)

        self.assertIn('造件已完成',china_code)
    # def test_first_second_supplement(self):
    #     request=HttpRequest()
    #     request.method='POST'
    #     request.POST['FIRST_SUPPLY_MATERIAL']
    #     request.POST['id']
    #     request.POST['mobile']
    #
    #
    # def test_django_test(self):
    #     request=HttpRequest()
    #     response=django_test(request)



