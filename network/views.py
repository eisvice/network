from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    print(request.POST)
    print(request.POST.get("post-content"))
    if request.method == "POST":
        if "submit-new-post" in request.POST:
            new_post = create_new_post(request)
            return JsonResponse({
                "message": "Post was successfully published",
                "twitt": new_post.serialize(),
                }, status=201)
        elif "like-post" in request.POST:
            pass
        else:
            return JsonResponse({"error": "Something wrong..."}, status=400)
    else:
        posts = Post.objects.all().order_by("-timestamp")
        return render(request, "network/index.html", {
            "posts": posts,
        })


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
