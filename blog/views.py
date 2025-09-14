from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
# from . import data
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm

# from .data import Post
#
# # Create your views here.
#
# data.seed()
#
#
# def post_list(request):
#     posts = data.all_posts()
#     q = request.GET.get('q')
#     if q:
#         q_low = q.lower()
#         posts = [p for p in posts if q_low in p.title.lower() or q_low in p.content.lower()]
#
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
#
# def post_detail(request, pid: int):
#     post = data.get_post(pid)
#     if not post:
#         return HttpResponseNotFound('Post did not find')
#     return render(request, 'blog/post_detail.html', {'post': post})
#
#
# def post_create(request):
#     print(request)
#     if request.method == 'GET':
#         return render(request, 'blog/post_form.html', {"mode": "create", "post": Post(0, "", "", "")})
#
#     # POST
#     title = (request.POST.get('title') or "").strip()
#     content = (request.POST.get('content') or "").strip()
#     author = (request.POST.get('author') or "").strip()
#
#     if not title or not content:
#         messages.error(request, 'Title and Content is required')
#         return render(request, 'blog/post_form.html',
#                       {"mode": "create", "title": title, "content": content, "author": author})
#
#     post = data.add_post(title, content, author)
#
#     messages.success(request, 'Post created successfully')
#     # return redirect('blog:post_detail',pid=post.id)
#     return redirect(reverse('blog:post_detail', args=[post.id]))
#
#
# def post_delete(request, pid: int):
#     post = data.get_post(pid)
#     if not post:
#         return HttpResponseNotFound('Post did not find')
#
#     if request.method == 'GET':
#         return render(request, "blog/post_confirm_delete.html", {"post": post})
#
#     ok = data.delete_post(pid)
#
#     if ok:
#         messages.success(request, 'Post deleted successfully')
#
#         return redirect(reverse('blog:post_list'))
#
#     return HttpResponseBadRequest("Error in delete operation")
#
#
# def post_search(request):
#     q = request.GET.get('q')
#     posts = data.all_posts()
#
#     if q:
#         q_low = q.lower()
#         posts = [p for p in posts if q_low in p.title.lower() or q_low in p.content.lower()]
#
#     return render(request, 'blog/post_list.html', {'posts': posts, "q": q})

from django.db.models import Q

def post_list(request):
    q=(request.GET.get('q') or "").strip()
    qs=Post.objects.all()
    if q:
        qs=qs.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).distinct()

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page') or 1
    page_obj=paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj':page_obj,
        'posts':page_obj.object_list,
        "q":q
        })

def post_search(request):
    return post_list(request)

def post_create(request):
    if request.method == "GET":
        form=PostForm()

        return render(request, 'blog/post_form.html', {'form':form,"mode":"create"})

    form=PostForm(request.POST)
    if form.is_valid():
        post=form.save()

        messages.success(request, "Post created successfully")
        return redirect('blog:post_detail',slug=post.slug)

    messages.error(request, "There were errors in Form")
    return render(request, 'blog/post_form.html', {'form':form,"mode":"create"})

def post_detail_by_pk(request, pk:int):
    post=get_object_or_404(Post,pk=pk) #ORM SELECT WHERE id=pk
    return render(request, 'blog/post_detail.html', {'post':post})

def post_detail_by_slug(request, slug:str):
    post=get_object_or_404(Post,slug=slug) #ORM SELECT WHERE slug=slug . . .
    return render(request, 'blog/post_detail.html', {'post':post})

def post_edit(request, pk:int):
    post=get_object_or_404(Post,pk=pk)
    if request.method == "GET":
        form=PostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form':form,"mode":"edit","post":post})
    form=PostForm(request.POST, instance=post)
    if form.is_valid():
        post=form.save() # ORM updated
        messages.success(request, "Post edited successfully")
        return redirect('blog:post_detail',slug=post.slug)

    messages.error(request, "There were errors in Form")
    return render(request, 'blog/post_form.html', {'form':form,"mode":"edit","post":post})

def post_delete(request, pk:int):
    post=get_object_or_404(Post,pk=pk)
    if request.method == "GET":
        return render(request, 'blog/post_confirm_delete.html', {'post':post})
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect('blog:post_list')

