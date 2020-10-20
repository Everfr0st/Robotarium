from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class CreatePost(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("USER>", request.user)
        print(request.data, request.POST)
        print(args)
        print(kwargs)

        return JsonResponse({'created':True})