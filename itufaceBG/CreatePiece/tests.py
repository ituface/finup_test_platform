from django.test import TestCase


from django.http import HttpRequest
from CreatePiece.views import add_piece_api


class AddPieceApiTest(TestCase):


    def test_add_piece_api_post_request(self):
        request=HttpRequest()
        request.method='POST'
        request.POST['name']='测试一'
        request.POST['mobile']='19429008888'
        request.POST['status']='PUSH_TO_IRON'
        request.POST['num']='1'
        request.POST['product_type']=''
        request.POST['saleNo']=''
        request.POST['salePassword']=''
        request.POST['year']=''
        request.POST['video_check']='OFF_SIGN'
        request.POST['idNo']=''

        response=add_piece_api(request)

        self.assertIn('造件已完成',response.content.decode())



