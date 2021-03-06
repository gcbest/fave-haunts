from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .models import Like
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

@login_required
# Create your views here.
def create(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['url']:
			post = Post()
			post.title = request.POST['title']
			if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
				post.url = request.POST['url']
			else:
				post.url = 'http://' + request.POST['url']
			post.pub_date = timezone.datetime.now()
			post.author = request.user
			post.topic = request.POST['topics']
			post.save()
			return redirect('home')
		else:
			return render(request, 'posts/create.html', {'error': 'ERROR: You must include a title and url to create a post'})
	else:
		return render(request, 'posts/create.html')

def home(request):
	posts = Post.objects.order_by('-votes_total')
	return render(request, 'posts/home.html', {'posts': posts})

def upvote(request, pk):
	if request.method == 'POST':
		post = Post.objects.get(pk=pk)
	
		number_of_likes = post.like_set.all().count()

		new_like, created = Like.objects.get_or_create(user=request.user, post=post)
		if not created:
			# the user already liked this post before
			print('already liked by this user')
		else:
			# first time liking the post
			print('new like')
			like = Like()
			like.user = request.user
			like.post = post
			post.votes_total += 1
		post.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def downvote(request, pk):
	if request.method == 'POST':
		post = Post.objects.get(pk=pk)
		post.votes_total -= 1
		post.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def userposts(request, fk):
	# filter posts by author
	posts = Post.objects.filter(author__id=fk).order_by('-votes_total')
	author = User.objects.get(pk=fk)
	print(request.user.id)
	return render(request, 'posts/userposts.html', {'posts': posts, 'author': author})

def upvoted(request, fk):
	likes = Like.objects.filter(user__id=fk)
	user = User.objects.get(pk=fk)
	return render(request, 'posts/upvoted.html', {'likes': likes, 'user': user})

@login_required
def food(request):
	# filter posts by topic
	posts = Post.objects.filter(topic='food').order_by('-votes_total')
	return render(request, 'posts/food.html', {'posts': posts, 'topic': 'Food'})

@login_required
def fun(request):
	# filter posts by topic
	posts = Post.objects.filter(topic='fun').order_by('-votes_total')
	return render(request, 'posts/fun.html', {'posts': posts, 'topic': 'Fun'})