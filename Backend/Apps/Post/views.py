from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_eventstream import send_event
from notify.signals import notify
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Apps.Post.models import Post, PostPhoto, TagUser
from Apps.User.models import UserProfilePhoto


class PostList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        post_list = []
        posts = Post.objects.all().order_by("-created")

        for post in posts:
            dic_post = {}
            user_pp = UserProfilePhoto.objects.filter(user_id=post.user.pk)
            if user_pp.exists():
                profile_picture = user_pp[0].profile_picture.url
            else:
                profile_picture = ''
            dic_post["name"] = '{0} {1}'.format(post.user.first_name, post.user.last_name)
            dic_post["username"] = post.user.username
            dic_post["profile_picture"] = profile_picture
            dic_post["content"] = post.body
            dic_post["created"] = post.created.strftime("%b %d, %Y")
            dic_post["photos"] = list(PostPhoto.objects.filter(post=post).values_list('photo', flat=True))
            dic_post["tag_users"] = list(User.objects.filter(
                id__in=list(
                    TagUser.objects.filter(post=post).values_list('user', flat=True)
                )
            ).values_list('username', flat=True)
                                         )
            post_list.append(dic_post)

        return JsonResponse(post_list, safe=False)


class CreatePost(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            content = request.POST["content"]
            num_photos = int(request.POST["num_photos"])
            num_users = int(request.POST["num_users"])
            user = User.objects.get(username=request.POST["username"])
            post = Post.objects.create(user=user, body=content)
            for i in range(0, num_photos):
                photo = request.FILES.get("photo_{}".format(i))
                PostPhoto.objects.create(post=post, photo=photo)

            for i in range(0, num_users):
                user = request.POST.get("user_{}".format(i))
                user = User.objects.get(username=user)
                TagUser.objects.create(post_id=post.pk, user_id=user.pk)
                self.tag_user(recipient=user, actor=request.user, target=post)
            self.notify_users()
            return JsonResponse({'created': True})
        except:
            return JsonResponse({'created': False})

    def tag_user(self, recipient, actor, target):
        notify.send(actor, recipient=recipient, actor=actor, target=target,
                    verb='te etiquetó en', nf_type='tagged_by_one_user')

    def notify_users(self):
        send_event('posts', 'notification', {'text': 'New post'})
