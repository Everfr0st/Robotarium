from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login

from ..Chat.models import Message


class SignUp(TemplateView):
    def get(self, request, **kwargs):  # change to Post Method
        try:
            username = self.request.GET["Username"]
            email = self.request.GET["Email"]
            role = self.request.GET["Role"]
            password = self.request.GET["Password"]

            user = User.objects.create(username=username, email=email)

            if role == "Estudiante":
                Student.objects.create(user=user)
            elif role == "Docente":
                Teacher.objects.create(user=user)

            user_to_authenticate = authenticate(
                username=username, password=password)
            login(request, user_to_authenticate)

            return JsonResponse({
                'SignUp': True,
                'Authenticated': True,
                'Rol': role,
            })

        except:
            user.delete()
            return JsonResponse({
                'SignUp': False,
                'Authenticated': False
            })


class SignUpMoreInfo(TemplateView):
    def get(self, request, **kwargs):  # Post Method

        try:
            role = self.request.GET["Role"]

            if role == "Estudiante":
                carreer = self.request.GET["Carreer"]
                semester = self.request.GET["Semester"]

                student = Student.objects.get(user=self.request.user)
                student.carreer = carreer
                student.semester = semester
                student.save()

            elif role == "Docente":
                department = self.request.GET["Department"]
                date_start = self.request.GET["Date_start"]

                teacher = Teacher.objects.get(user=self.request.user)
                teacher.department = department
                teacher.date_start = date_start

            return JsonResponse({
                'SignUp': True,
            })
        except:
            return JsonResponse({
                'SignUp': False,
            })


class SignIn(TemplateView):
    def get(self, request, **kwargs):
        try:
            username = request.GET["Username"]
            password = request.GET["Password"]

            user_to_authenticate = authenticate(
                username=username, password=password)
            login(request, user_to_authenticate)
            # http://127.0.0.1:8000/login/?Username=pipe&Password=Coco_F13280212
            return JsonResponse({
                'Authenticated': True
            })

        except:
            return JsonResponse({'Authenticated': False, })


class NavBar(TemplateView): #, LoginRequiredMixin):
    #login_url = '/'

    def get(self, request, **kwargs):
        #user = request.user
        user = User.objects.get(id=1)
        try:
            profile_picture = UserProfilePhoto.objects.get(
                user_id=user.pk).profile_picture.url
        except:
            profile_picture = ''
        unread_messages = Message.objects.filter(
            (Q(conversation__owner_id=request.user.pk) |
             Q(conversation__opponent_id=request.user.pk)),
            read=False
        ).exists()
        unread_notifications = True
        return JsonResponse({
            'name': user.username,
            'profile_picture': profile_picture,
            'unread_messages': unread_messages,
            'unread_notifications': unread_notifications
        })


class LogOut(LogoutView):
    pass
