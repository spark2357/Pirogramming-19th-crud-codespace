from django.shortcuts import render

def hello_world(request):
    return render(request, "posts/hello_world.html")