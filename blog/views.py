from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Quest
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms1 import ContactForm
from django.shortcuts import redirect

posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
	
def post_new(request):
	form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})
	
def quest_new(request):
	form = ContactForm()
	return render(request, 'blog/quest_edit.html', {'form': form})
	
def quest_edit1(request):
	form = ContactForm()
	return render(request, 'blog/quest_edit1.html', {'form': form})
	
def quest_new(request):
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return render(request, 'blog/quest_edit1.html')
	else:
		form = ContactForm()
	return render(request, 'blog/quest_edit.html', {'form': form})
	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})
	
def post_app(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})