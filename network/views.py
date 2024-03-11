import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    if request.method == "POST":
        if "submit-new-post" in request.POST:
            new_post = create_new_post(request)
            new_post.save()
            return HttpResponseRedirect(reverse("index"))
        elif "edit-post" in request.POST:
            data = json.loads(request.POST["document"])
            existed_posts = [i.id for i in Post.objects.filter(user=request.user)]
            if data["author"] == request.user.username and int(data["id"]) in existed_posts and data["body"] != Post.objects.get(pk=int(data["id"])).body:
                existed_post = Post.objects.get(pk=int(data["id"]))
                existed_post.body = data["body"]
                existed_post.save(update_fields=["body"])
                return JsonResponse({"message": "Post was successfully updated!"}, status=201)
            return JsonResponse({"message": "Canceled"}, status=201)
    elif request.method == "PUT":
        return save_like(request)
    else:
        posts_q = Post.objects.all().order_by("-timestamp")
        paginator = Paginator(posts_q, 10)
        page_number = request.GET.get("page")
        posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": posts,
        })
        
        
def following(request):
    if request.method == "PUT":
        return save_like(request)
    else:
        followings = User.objects.all().filter(follows=request.user)
        posts_q = Post.objects.filter(user__in=followings).order_by("-timestamp")
        paginator = Paginator(posts_q, 10)
        page_number = request.GET.get("page")
        posts = paginator.get_page(page_number)
        return render(request, "network/following.html", {
            "posts": posts,
        })


def profile(request, profile):
    follower = User.objects.get(username=profile)
    following = User.objects.all().filter(follows=request.user)
    if request.method == "POST":
        if "edit-post" in request.POST:
            data = json.loads(request.POST["document"])
            existed_posts = [i.id for i in Post.objects.filter(user=request.user)]
            if data["author"] == request.user.username and int(data["id"]) in existed_posts and data["body"] != Post.objects.get(pk=int(data["id"])).body:
                existed_post = Post.objects.get(pk=int(data["id"]))
                existed_post.body = data["body"]
                existed_post.save(update_fields=["body"])
                return JsonResponse({"message": "Post was successfully updated!"}, status=201)
            return JsonResponse({"message": "Canceled"}, status=201)
        else:
            data = json.loads(request.body)
            follows = data.get("follower")
            if follows and request.user not in follower.follows.all():
                follower.follows.add(request.user)
                return JsonResponse({"message": f"You have followed to {profile}"}, status=201)
            elif not follows and request.user in follower.follows.all():
                follower.follows.remove(request.user)
                return JsonResponse({"message": f"You have unfollowed from {profile}"}, status=201)
    elif request.method == "PUT":
        return save_like(request)
    else:
        posts_q = Post.objects.all().order_by("-timestamp").filter(user=User.objects.get(username=profile))
        paginator = Paginator(posts_q, 10)
        page_number = request.GET.get("page")
        posts = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "posts": posts,
            "profile": profile,
            "followers": follower.follows.all(),
            "followings": following,
        })


def save_like(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    liked = data.get('liked')
    post = Post.objects.get(pk=post_id)
    if liked == 'false':
        post.likes_count.remove(request.user)
    elif liked == 'true':
        post.likes_count.add(request.user)
    return HttpResponse(status=204)


def create_new_post(request):
    new_post = Post.objects.create(
        user=request.user, 
        body=request.POST["post-content"]
    )
    return new_post


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
