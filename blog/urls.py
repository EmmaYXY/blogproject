from django.conf.urls import url
from . import views # . 表示当前目录


#网址和处理函数的关系，index为处理函数，name是处理函数的别名
app_name = 'blog'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]