from ..models import Post, Category
from django import template

from django.db.models.aggregates import Count # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
from blog.models import Category


register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
	return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
	# 双下划线是查询表达式
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts_gt=0)


