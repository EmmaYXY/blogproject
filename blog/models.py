from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

	# 文章创建时间和最后一次修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	excerpt = models.CharField(max_length=200, blank=True)

	# 文章的数据库表和分类、标签的数据库表关联起来，但要根据需求采取不同
	# 的关联方式
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)

	# 关联 Django 内置应用 django.contrib.auth 中的用户模型 User
	# on_delete=models.DO_NOTHING 是另一个选择，但不要忘记这个参数
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk':self.pk})

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	def save(self, *args, **kwargs):
		# 如果没有填写摘要
		if not self.excerpt:
			# 先实例化一个 Markdown 的类，用于渲染 body 的文本
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
				# 先将 Markdown 文本渲染成 HTML 文本
				# strip_tags 去掉 HTML 文本的全部HTML标签
				# 从文本摘取前 54 个字符赋给 excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:54]

			# 调用父类 save 方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created_time']


# Create your models here.
