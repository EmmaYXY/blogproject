from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
		

class Post(models.Model):
	title = models.CharField(max_length=70)

	body = models.TextField()

	#文章创建时间和最后一次修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	excerpt = models.CharField(max_length=200, blank=True)

	#文章的数据库表和分类、标签的数据库表关联起来，但要根据需求采取不同
	#的关联方式
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)

	#关联Django内置应用django.contrib.auth中的用户模型User
	#on_delete=models.DO_NOTHING是另一个选择，但不要忘记这个参数
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

# Create your models here.