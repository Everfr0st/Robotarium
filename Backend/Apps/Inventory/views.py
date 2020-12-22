import json

from django.db.models import Q
from rest_framework import generics, status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rasweb.mailing import sendMail
from .models import *
from .serializer import InventorySerializer, ReserveSerializer


class InventoryListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = InventorySerializer
    model = Inventory

    def get_queryset(self):
        return Inventory.objects.filter(code__icontains=self.request.GET["code"]).order_by("-code")


class ItemDetailApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = InventorySerializer
    model = Inventory

    def get_queryset(self):
        return Inventory.objects.filter(code__icontains=self.request.GET["code"]).order_by("-code")


class ReserveListApi(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    model = Reserve

    def get(self, request, *args, **kwargs):
        query_list = []
        date = request.GET["date"]
        code = request.GET["code"]
        name = request.GET["name"]

        reservations = self.get_queryset([date, name, code])
        for reservation in reservations:
            query_list.append(reservation.serializer())
        return JsonResponse(query_list, safe=False)

    def get_queryset(self, params):
        return Reserve.objects.filter(
            schedule__date=params[0],
            element__name__icontains=params[1],
            element__code=params[2]
        ).order_by("code")


class CreateReservationApi(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        data = json.loads(request.data)
        schedule = data["schedule"]
        element = data["element"]
        user = data["user"]

        schedule_record, element_in_db, user_in_db, reservation = None, None, None, None
        try:
            schedule_record = Schedule.objects.get(
                date=schedule["date"],
                start_time=schedule["start"],
                end_time=schedule["end"]
            )
        except Schedule.DoesNotExist:
            schedule_record = Schedule.objects.create(
                date=schedule["date"],
                start_time=schedule["start"],
                end_time=schedule["end"]
            )
        try:
            element_in_db = Inventory.objects.get(
                name=element["name"],
                code=element["code"]
            )
        except Inventory.DoesNotExist:
            pass
        try:
            user_in_db = User.objects.get(username=user["username"])
        except User.DoesNotExists:
            pass
        reservation = Reserve.objects.create(
            user=user_in_db,
            schedule=schedule_record,
            element=element_in_db,
            quantity=element_in_db.quantity,
        )
        self.mail_configs(reservation)
        try:

            return JsonResponse({'created': True})
        except:
            return JsonResponse({'created': False})

    def mail_configs(self, reservation):
        username = reservation.user.username
        subject = '{0} {1}, reservaste el elemento {2} en la ubicación {3}'.format(
            reservation.user.first_name,
            reservation.user.last_name,
            reservation.element.name,
            reservation.element.code
        )
        try:
            date_formated = reservation.schedule.date.strftime("%d de %b. de %Y")
            start_formated = reservation.schedule.start_time.strftime("%I :%M %p")
            end_formated = reservation.schedule.end_time.strftime("%I:%M %p")
        except:
            date_formated = datetime.strptime(reservation.schedule.date, '%Y-%m-%d').strftime("%d de %b. de %Y")
            start_formated = str(reservation.schedule.start_time)[0:len(str(reservation.schedule.start_time)) - 3]
            end_formated = str(reservation.schedule.end_time)[0:len(str(reservation.schedule.start_time)) - 3]

        description = 'Descarga el archivo con formato .ics y sincroniza tu calendario con el evento que tienes el {0} de {1} a {2}' \
            .format(
            date_formated,
            start_formated,
            end_formated
        )
        context = {
            'username': username,
            'subject': subject,
            'description': description

        }
        configs = {
            'Template': 'MailTemplates/reservation-mail.html',
            'subject': 'Detalles de tu reserva',
            'to': [reservation.user.email],
        }
        file_configs = {
            'file_name': 'reservation-{0}{1}.ics'.format(reservation.user.first_name, reservation.pk),
            'content': reservation.generate_event(),
            'type': 'text/calendar'
        }
        sendMail(configs, context, file_configs)


class ReservationHistoryApi(generics.ListAPIView):
    model = Reserve
    serializer_class = ReserveSerializer

    def get_queryset(self):
        query = self.request.GET.get("query")
        date_start = self.request.GET.get("dateStart")
        date_end = self.request.GET.get("dateEnd")
        return Reserve.objects.filter(element__name=query, schedule__date__gte=date_start, schedule__date__lte=date_end)
