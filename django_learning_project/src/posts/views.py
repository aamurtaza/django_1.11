from urllib.parse import quote  
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import PostForm
from .models import Post


def post_create(request):
    # If reuqest also submiting files then adding "request.FIlES" is necessary
    form = PostForm(request.POST or None, request.FILES or None)  
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Post successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Post not successfully created.")
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,

    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "title": "List",
        "page_request_var":  page_request_var
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug =slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post updated")
        # For tags understanding
        # messages.success(request, "<a href='#'>Item</a> Saved",
        # extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Post successfully deteted")
    return redirect("posts:list")
