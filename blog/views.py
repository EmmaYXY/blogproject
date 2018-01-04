from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category

import markdown

from django.views.generic import ListView, DetailView

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from comments.forms import CommentForm


class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	# 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
	paginate_by = 10


	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
    		# 没有分页，则不需任何分页导航条数据，返回空字典
			return {}

    	# 当前页左,右边连续的页码号，初始值为空
		left = []
		right = []

    	# 第 1 页,最后一页页码后是否需要显示省略号
		left_has_more = False
		right_has_more = False

    	# 是否需要显示第一页，最后一页的页码号
    	# 如果当前页左边连续页码号包含边界页面，则无需显示
		first = False
		last = False

    	# 获得用户当前请求页码号
		page_number = page.page_number

    	# 获得分页后总页数
		total_pages = paginator.num_pages

    	# 获得整个分页页码列表，比如分了四页，就是 [1, 2, 3, 4]
		page_range = paginator.page_range

		if page_number == 1:
    		# 用户请求第一页数据，left=[]，只需要当前页右边连续页码号
    		# 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]
    		# 也可改变数字，获取更多页码
			right = page_range[page_number:page_number + 2]

    		# 如果最右边页码号比最后一页页码号减去 1 还要小
    		# 即需要显示省略号，通过 right_has_more 来指示
			if right[-1] < total_pages - 1:
				right_has_more = True

    		# 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
    		# 所以需要显示最后一页的页码号，通过 last 来指示
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True

		else:
    		# 用户请求中间页码，需要当前页左右两边的连续页码号
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
    		'left': left,
    		'right': right,
    		'left_has_more': left_has_more,
    		'right_has_more': right_has_more,
    		'first': first,
    		'last': last,
    	}
		return data


	def get_context_data(self, **kwargs):
		"""
		在试图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
		在类视图中，这个字典是通过 get_context_data 获得的，
		所以覆写该方法，是以让我们额能够再插入一些自定义的模板变量进去
        """

        # 首先获得父类生成的传递给模板的字典
		context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_boj、is_paginated 三个模板变量
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		# 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		# 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典
		context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典里的模板变量去渲染模板
		return context

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
		md = markdown.Markdown(extensions=['markdown.extensions.extra',
								           'markdown.extensions.codehilite',
								           TocExtension(slugify=slugify),
								           ])
		post.body = md.convert(post.body)
		post.toc = md.toc
		return post

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



class TagView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		tag =  get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)		     



def search(request):
	q = request.GET.get('q')
	error_msg = ''

	if not q:
		error_msg = '请输入关键词'
		return render(request, 'blog/index.html', {'error_msg':error_msg})

	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))	
	return render(request, 'blog/index.html', {'error_msg': error_msg,
											   'post_list': post_list})	         


# Create your views here.
