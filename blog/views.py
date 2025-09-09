from django.http import HttpResponse
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
