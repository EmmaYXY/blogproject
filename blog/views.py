from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return render(request, 'blog/index.html', content={
		                   'title':'我的博客首页', 
		                   'welcome':'23333，居然真得有人来访问本宫的博客！'
		          })


# Create your views here.
