from django.shortcuts import render, redirect
from .models import *

from django.http.request import HttpRequest
from django.db.models import Q

def hello_world(request):
    return render(request, "posts/hello_world.html")

def posts_list(request: HttpRequest, *args, **kwargs):
    
    # 값이 없을 경우에 오류가 납니다.
    # text = request.GET["text"]
    # 값이 없을 경우에 None 반환합니다.
    text = request.GET.get("text")
    min = request.GET.get("min_price")
    max = request.GET.get("max_price")

    posts = Post.objects.all()
    
    if text:
        # 장고 쿼리셋 lookup
        # or만 Q로 해주면 되고, and조건은 그냥 쉼표로 연결.
        posts = posts.filter(Q(title__contains=text) or Q(content__contains=text))
    
    if min and max and min <= max:
        posts = posts.filter(price__gte=min, price__lte=max)
    elif min:
        posts = posts.filter(price__gte=min)
    elif max:
        posts = posts.filter(price__lte=max)

    return render(request, "posts/posts_list.html", {"posts":posts})

# 한 게시글 읽는 Read
def posts_read(request: HttpRequest, pk, *args, **kwargs):
    post = Post.objects.get(id=pk)
    print(post)

    # 현재 글에 이미 좋아요를 눌렀나? 이미 눌렀으면 like에 뭐가 들어있음.
    # 근데 안 눌렀으면 like에 None이 들어가 있을 것.
    # get을 안 쓰고 filter를 쓴 이유 : get은 아무것도 없으면 오류가 나서.
    like = Like.objects.filter(post_id=pk).first()

    if request.method == "POST":
        if like == None:
            Like.objects.create(post_id=pk)
        else:
            # 좋아요 해제
            like.delete()
        return redirect(f"/posts/{pk}")

    return render(request, "posts/posts_read.html", {"post":post, "like":like})

# create를 만들자
def posts_create(request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
        Post.objects.create(
                title=request.POST["title"],
                user=request.POST["user"],
                region=request.POST["region"],
                price=request.POST["price"],
                content=request.POST["content"],
            )
        return redirect("/")
    return render(request, "posts/posts_create.html")

def posts_delete(request: HttpRequest, pk, *args, **kwargs):
    # DELETE / PUT... -> REST API
    # 삭제해야 할 때 -> 삭제하기 버튼 눌러서 POST로 왔을 때
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.delete()

    return redirect("/")

def posts_update(request: HttpRequest, pk, *args, **kwargs):

    post = Post.objects.get(id=pk)

    if request.method == "POST":
        # 수정하는 부분
        post.title = request.POST["title"]
        post.user = request.POST["user"]
        post.region = request.POST["region"]
        post.price = request.POST["price"]
        post.content = request.POST["content"]
        post.save()
        return redirect(f"/posts/{post.id}")

    return render(request, "posts/posts_update.html", {"post":post})

# 좋아요 목록 페이지
def posts_like(request, *args, **kwargs):

    likes = Like.objects.all()

    posts = []
    # likes : 좋아요 한 글들의 id의 쿼리셋
    # posts : 좋아요 한 글들의 리스트
    for like in likes:
        # like.post_id : 좋아요 한 글의 id
        posts.append(Post.objects.get(id=like.post_id))

    return render(request, "posts/posts_like.html", {"posts":posts})


# 보통 쓰는 곳
# get : 값을 변경하지 않는 요청들, 주로 검색
# post : 사용자가 값을 변경하는 요청들

# get : url?a=b=c= 누구나 쉽게 볼 수 있다. 글자수의 한계가 있다.
# post : 쉽게 값을 보기 어렵고, 글자수 한계도 거의 없다.