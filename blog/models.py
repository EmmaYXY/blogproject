from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=100)


class Tag(models.Model):
	name = models.CharField(max_length=100)
		

class Post(models.Model):
	title = models.CharField(max_length=70)

	body = models.TextField()

	#文章创建时间和最后一次修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	excerpt = models.CharField(max_length=200, blank=True)

	#文章的数据库表和分类、标签的数据库表关联起来，但要根据需求采取不同
	#的关联方式
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag, blank=True)

	#关联Django内置应用django.contrib.auth中的用户模型User
	author = models.ForeignKey(User)

# Create your models here.
