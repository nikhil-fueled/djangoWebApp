# Create your views here.
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render,get_object_or_404, redirect
from blog.models import Post, Comment
from django.contrib import auth

def index(request):
	user= request.user
	print user
	posts= Post.objects.all().order_by("-created")
	paginator= Paginator(posts, 2)
	try:
		page=int(request.GET.get("page",'1'))
	except ValueError:
		page=1
	try:
		posts= paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts= paginator.page(paginator.num_pages)
	return render(request,'blog/list.html', {"posts":posts, "user":user})

def addComment(request):
	post1= get_object_or_404(Post, pk=request.GET['post'])
	comment= Comment(name=request.GET['name'], body= request.GET['comments'], post=post1)
	comment.save()
	print comment
	return index(request)

def view(request, pk):
	post= Post.objects.get(pk=pk)
	print post
	comment= Comment.objects.all()
	print comment
	return render(request, 'blog/view.html', {"post": post, "comments": comment})

def login(request):
	print "loggin in--------"
	username= request.POST['username']
	password=request.POST['password']
	user=auth.authenticate(username=username, password=password)
	request.user=user
	if user is not None:
		print "logged"
	else:
		print "not logged in"
	return redirect('/blog', request)

def logout(request):
	auth.logout(request)
	return redirect('/blog')