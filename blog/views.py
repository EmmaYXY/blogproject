from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
import markdown
from django.views.generic import ListView, DetailView


class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

"""
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.increase_views()
	post.body = markdown.markdown(post.body,
								  extensions=['markdown.extensions.extra',
								  			  'markdown.extensions.codehilite',
								  			  'markdown.extensions.toc',
								  ])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post':post,
			   'form':form,
			   'comment_list':comment_list
			   }
	return render(request, 'blog/detail.html', context=context)
"""

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self, request, *args, **kwargs):
		# 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
		# get 方法返回一个HttpResponse 实例
		# 之所以需哟啊先调用父类 get 方法，是因为只有当 get 方法被调用后，
		# 才有 self.object 属性，其值为 Post 模型实例， 即被访问的文章post
		response = super(PostDetailView, self).get(request, *args, **kwargs)

		# 将文章阅读量 +1
		# 注意 self.object 的值就是被访问的文章 post
		self.object.increase_views()

		# 视图必须返回一个 HttpResponse 对象
		return response

	def get_object(self, queryset=None):
		#覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
		post = super(PostDetailView, self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,
								      extensions=[
								           'markdown.extensions.extra',
								           'markdown.extensions.codehilite',
								           'markdown.extensions.toc',
								           ])
		return post_list

	def get_context_data(self, **kwargs):
		# 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DtailView 以及帮我们完成），
		# 还要把评论表单	post 下的评论列表传递给模板。
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list
			})
		return context


# def archives(request, year, month):
	# post_list = Post.objects.filter(created_time__year=year,
									# created_time__month=month)
	# return render(request, 'blog/index.html', context={'post_list': post_list})

class ArchivesView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
			                                                   created_time__month=month
			                                                   )

class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)


		                 
		         


# Create your views here.
