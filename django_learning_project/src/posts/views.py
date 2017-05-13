from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import PostForm
from .models import Post

def post_create(request):
	form = PostForm(request.POST or None) 
	if form.is_valid():
		instance = form.save(commit=False)
		print (form.cleaned_data.get("title"))
		instance.save()
	#not recommended
	# if request.method == "POST":
	# 	print (request.POST.get("content"))
	# 	print (request.POST.get("title"))
		# Post.objects.create(title=title) 
	context = {
		"form":form,
	}

	return render(request, "post_form.html", context)

def post_detail(request , id=None): #retrieve
	# instance = Post.objects.get(id=5)
	instance = get_object_or_404(Post, id = id)
	context  = {
		"title" : instance.title,
		"instance":instance
	}
	return render(request, "post_detail.html", context)

def post_list(request): #list items
	queryset = Post.objects.all()
	context  = {
		"queryset":queryset,
		"title" : "List"
	}		
	
	# if request.user.is_authenticated():
	# 	context  = {
	# 		"title" : "User list"
	# 	}
	# else:
	# 	context  = {
	# 		"title" : "List"
	# 	}
	return render(request, "index.html", context)
	# return HttpResponse("<h1>List</h1>")

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")
