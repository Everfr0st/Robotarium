from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Apps.Post.models import Post, PostPhoto


def CreatePost(request):
    if request.method == "POST":
        content = request.POST["content"]
        num_photos = int(request.POST["num_photos"])
        user = User.objects.get(username=request.POST["username"])
        post = Post.objects.create(user=user, body=content)
        for i in range(0,num_photos):
            photo = request.FILES.get("photo_{}".format(i))
            PostPhoto.objects.create(post=post, photo=photo)

    return JsonResponse({'created': True})
