"""itufaceBG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from AppManage import views
from AppApi import  views as apiview
from CreatePiece import views as pieceview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'app-list', views.app_list,name='app-list'),
    url(r'^del_app_list/', views.del_app_list,name='del_app_list'),
    url(r'add-app/', views.add_app,name='add-app'),
    url(r'^login/', views.index),
    url(r'update-app/', views.update_app,name='update-app'),
    url(r'qr-ios-download/',views.qr_ios_download),
    url(r'^index/$',apiview.index),
    url(r'welcome',apiview.welcome),
    url(r'piece-list',pieceview.piece_list,name='piece-list'),
    url(r'^add-piece',pieceview.add_piece),
    url(r'api-add-piece',pieceview.add_piece_api,name='api-add-piece'),
    url(r'app-product',pieceview.app_product),
    url(r'add-product',pieceview.add_product),
    url(r'del_product_list',pieceview.del_product_list,name='del_product_list'),
    url(r'del_piece_list',pieceview.del_piece_list,name='del_piece_list'),
    url(r'finup_lottery',views.finup_lottery,name='finup_lottery'),

]
