from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)

	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid():
			# 检查到数据是合法的，调用表单的save方法保存数据到数据库
			# 参数的作用是，仅利用表单的数据生产Comment模型类的实例，还未保存至数据库
			comment = form.save(commit=False)

			# 将评论和被评论的文章关联起来
			comment.post = post

			comment.save()

			# 重定向到post的详情页，实际上当redirect函数接受一个模型的实例时，它会调用这个模型实例的
			# get_absolute_url方法，然后重定向到get_absolute_url方法返回的URL
			return redirect(post)
		else:
			# 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
			comment_list = post.comment_set.all()
			context = {'post': post,
					   'form': form,
					   'comment_list': comment_list
					   }
			return render(request, 'blog/detail.html', context=context)

	# 不是post请求，说明用户没有提交数据，重定向到文章详情页
	return redirect(post)



# Create your views here.
