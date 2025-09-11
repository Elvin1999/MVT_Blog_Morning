from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from . import data
# Create your views here.

data.seed()
def post_list(request):
    posts=data.all_posts()
    q=request.GET.get('q')
    if q:
        q_low=q.lower()
        posts=[p for p in posts if q_low in p.title.lower() or q_low in p.content.lower()]

    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request,pid:int):
    post=data.get_post(pid)
    if not post:
        return HttpResponseNotFound('Post did not find')
    return render(request,'blog/post_detail.html',{'post':post})
















