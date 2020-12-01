import json

from django.db.models import Q
from rest_framework import generics, status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        return Inventory.objects.filter(code__icontains=self.request.GET["code"]).order_by("code")


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
        )


class CreateReservationApi(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
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
        try:
            Reserve.objects.create(
                user=user_in_db,
                schedule=schedule_record,
                element=element_in_db,
                quantity=element_in_db.quantity,
            )
            return JsonResponse({'created': True})
        except:
            return JsonResponse({'created': False})


