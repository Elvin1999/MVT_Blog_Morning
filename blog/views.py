from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from . import data
from django.urls import reverse
from django.contrib import messages

from .data import Post

# Create your views here.

data.seed()


def post_list(request):
    posts = data.all_posts()
    q = request.GET.get('q')
    if q:
        q_low = q.lower()
        posts = [p for p in posts if q_low in p.title.lower() or q_low in p.content.lower()]

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pid: int):
    post = data.get_post(pid)
    if not post:
        return HttpResponseNotFound('Post did not find')
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    print(request)
    if request.method == 'GET':
        return render(request, 'blog/post_form.html', {"mode": "create", "post": Post(0, "", "", "")})

    # POST
    title = (request.POST.get('title') or "").strip()
    content = (request.POST.get('content') or "").strip()
    author = (request.POST.get('author') or "").strip()

    if not title or not content:
        messages.error(request, 'Title and Content is required')
        return render(request, 'blog/post_form.html',
                      {"mode": "create", "title": title, "content": content, "author": author})

    post = data.add_post(title, content, author)

    messages.success(request, 'Post created successfully')
    # return redirect('blog:post_detail',pid=post.id)
    return redirect(reverse('blog:post_detail', args=[post.id]))


def post_delete(request, pid: int):
    post = data.get_post(pid)
    if not post:
        return HttpResponseNotFound('Post did not find')

    if request.method == 'GET':
        return render(request, "blog/post_confirm_delete.html", {"post": post})

    ok = data.delete_post(pid)

    if ok:
        messages.success(request, 'Post deleted successfully')

        return redirect(reverse('blog:post_list'))

    return HttpResponseBadRequest("Error in delete operation")


def post_search(request):
    q = request.GET.get('q')
    posts = data.all_posts()

    if q:
        q_low = q.lower()
        posts = [p for p in posts if q_low in p.title.lower() or q_low in p.content.lower()]

    return render(request, 'blog/post_list.html', {'posts': posts, "q": q})
