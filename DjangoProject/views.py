from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello World!")

# def home(request):
#     context={"name":"Elvin","course":"Python web"}
#     return render(request,"home.html",context)

def home(request,username="User"):
    context={"name":username,"course":"Python web"}
    return render(request,"home.html",context)

def students(request):
    context={
        "students":["Elvin","Aysel","Murad"],
        "show":True
    }
    return render(request,"students.html",context)