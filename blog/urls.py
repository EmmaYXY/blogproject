from django.conf.urls import url
from . import views # . 表示当前目录


# 网址和处理函数的关系，index为处理函数，name是处理函数的别名
app_name = 'blog'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'post/(?P<pk>[0-9]+)/', views.PostDetailView.as_view(), name='detail'),
	url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/', views.ArchivesView.as_view(), name='archives'),
	url(r'category/(?P<pk>[0-9]+)/', views.CategoryView.as_view(), name='category'),
	url(r'tag/(?P<pk>[0-9]+)/', views.TagView.as_view(), name='tag'),
	url(r'about/', views.aboutview, name='about')
	# url(r'^search/$', views.search, name='search'),
]