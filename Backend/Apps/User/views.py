from PIL.Image import Image
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import TemplateView
from notify.models import Notification
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rasweb.settings import DOMAIN_BASE, BASE_DIR
from .auxmethods import get_semester_name
from .models import *
from .serializer import UserSerializer
from ..Chat.models import Message


class CreateUserApi(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            response = self.get_token_for_user(user)
            return JsonResponse(response)
        except:
            return Response({'status': 'Ya existe una cuenta asociada a este correo o nombre de usuario'}, status=409)

    def get_token_for_user(self, user):
        token = Token.objects.create(user=user)
        return {
            'created': True,
            'key': token.key
        }


class SignUpMoreInfo(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            response_obj = Student.objects.filter(user=request.user).first()

        except:
            response_obj = Teacher.objects.filter(user=request.user).first()

        if response_obj:
            return Response(response_obj.serializer(), status=200)
        else:
            return Response({'Detail': 'User rol not found'})

    def put(self, request, **kwargs):  # Post Method
        try:
            role = self.request.data["role"]
            if role == "Estudiante":
                career = self.request.data["career"]
                semester = self.request.data["semester"]
                try:
                    student = Student.objects.get(user=self.request.user)
                    student.career = career
                    student.semester = semester
                    student.save()
                except:
                    Student.objects.create(user=self.request.user, career=career, semester=semester)

            elif role == "Docente":
                department = self.request.data["department"]
                date_start = self.request.data["date_start"]
                try:
                    teacher = Teacher.objects.get(user=self.request.user)
                    teacher.department = department
                    teacher.date_start = date_start
                    teacher.save()
                except:
                    Teacher.objects.create(user=self.request.user, department=department, date_start=date_start)
            return Response({'Detail': 'User more info saved into DB'}, status=200)
        except:
            return Response({'Detail': 'User more info cannot be saved'}, status=500)


class NavBar(generics.RetrieveAPIView):  # , LoginRequiredMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        user = request.user
        try:
            profile_picture = UserProfilePhoto.objects.get(
                user_id=user.pk).profile_picture.url
        except:
            profile_picture = ''
        unread_messages = Message.objects.filter(
            (Q(conversation__owner_id=request.user.pk) |
             Q(conversation__opponent_id=request.user.pk)),
            read=False
        ).exclude(sender__username=user.username).count()
        unread_notifications = Notification.objects.filter(recipient_id=self.request.user.pk,
                                                           read=False).count()
        return JsonResponse({
            'username': user.username,
            'name': user.first_name + ' ' + user.last_name,
            'profile_picture': profile_picture,
            'unread_messages': unread_messages,
            'unread_notifications': unread_notifications
        })


class UsersList(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        domain = "http://127.0.0.1:8000"
        users_list = []
        users_query = User.objects.all().order_by("username")
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


class UserInfoApi(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        try:
            user_profile = UserProfilePhoto.objects.get(user_id=user_id)
            profile_picture = DOMAIN_BASE + user_profile.profile_picture.url
            user = user_profile.user
        except:
            profile_picture = ''
            user = User.objects.get(id=user_id)

        name = user.first_name + ' ' + user.last_name
        json_obj = {
            'name': name,
            'username': user.username,
            'profile_picture': profile_picture
        }
        return Response(json_obj)


class ProfilePictureApi(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        profile_picture = request.FILES.get("profile_picture")
        try:
            profile_picture_obj = UserProfilePhoto.objects.create(user=request.user, profile_picture=profile_picture)
            self.resize_img(profile_picture_obj)
            return Response({'profile_picture_created': True}, status=200)
        except:
            return Response({'profile_picture_created': False}, status=500)

    def put(self, request, *args, **kwargs):
        profile_picture = request.FILES.get("profile_picture")
        try:
            profile_picture_obj = UserProfilePhoto.objects.get(user=request.user)
            profile_picture_obj.profile_picture = profile_picture
            profile_picture_obj.save()
            self.resize_img(profile_picture_obj)
            return Response({'Detail': 'Profile photo updated successfully'}, status=200)
        except:
            self.post(request, args, kwargs)
        return Response({})

    def resize_img(self, profile_picture):
        import cv2 as cv
        path = str(BASE_DIR) + '/Files/' + str(profile_picture.profile_picture)
        img = cv.imread(path)
        height, width = img.shape[:2]

        # if ratio eidth/heigth is greater than 0.1, crop image (square format)
        if abs(height / width - 1) > 0.1:
            if height < width:
                image = img[0: height, int(width / 2) - int(height / 2): int(width / 2) + int(height / 2)]

            else:
                image = img[int(height / 2) - int(width / 2): int(height / 2) + int(width / 2), 0: width]

            # save current profile_picture in its path
            # encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
            # result, encimg = cv.imencode('.jpg', image, encode_param)
            cv.imwrite(path, image)
            im = Image.open(path)
            im.save(path, format="JPEG", quality=50)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class Logout(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        user_online = UserOnline.objects.get(user_id=request.user.pk)
        user_online.is_online = False
        user_online.save()
        return JsonResponse({'logout': True})
