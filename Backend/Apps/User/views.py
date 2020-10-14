from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.contrib.auth.models import User

from .auxmethods import get_semester_name
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


class NavBar(TemplateView):  # , LoginRequiredMixin):
    # login_url = '/'

    def get(self, request, **kwargs):
        # user = request.user
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
        ).count()
        unread_notifications = 3
        return JsonResponse({
            'username': user.username,
            'name': user.first_name + ' ' + user.last_name,
            'profile_picture': profile_picture,
            'unread_messages': unread_messages + 1,
            'unread_notifications': unread_notifications
        })


class UsersList(TemplateView):
    def get(self, request, **kwargs):
        # user = request.user
        domain = "http://127.0.0.1:8000"
        users_list = []
        users_query = User.objects.all()

        for user in users_query:
            user_dic = {
                "name": "{0} {1}".format(user.first_name,
                                         user.last_name).strip(" "),
                "username": user.username,
                "online": UserOnline.objects.get(user_id=user.pk).is_online
            }

            try:
                profile_picture = domain + UserProfilePhoto.objects.get(user_id=user.pk).profile_picture.url
            except:
                profile_picture = ''
            user_dic["profile_picture"] = profile_picture
            if user_dic["online"]:
                user_dic["color"] = "green"
            else:
                user_dic["color"] = "grey"
            users_list.append(user_dic)
        return JsonResponse(users_list, safe=False)


class UserDetail(TemplateView):
    def get(self, request, **kwargs):
        username = request.GET["username"]
        first_element = ''
        second_element = ''

        try:
            user_is_teacher = Teacher.objects.get(user__username=username)
            first_element = "Departamento de " + user_is_teacher.department
            second_element = "Trabaja desde el " + str(user_is_teacher.date_start.strftime("%d de %b de %Y"))
        except:
            try:
                user_is_student = Student.objects.get(user__username=username)
                first_element = "Estudiante de -" + user_is_student.career
                second_element = get_semester_name(user_is_student.semester)
            except:
                print("Error")

        return JsonResponse({
            'first_element': first_element,
            'second_element': second_element}
        )


class LogOut(LogoutView):
    pass
