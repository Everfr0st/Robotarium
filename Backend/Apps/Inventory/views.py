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
        return Inventory.objects.filter(code__icontains=self.request.GET["code"]).order_by("code")


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

        reservations = self.get_queryset([date,name,code])
        for reservation in reservations:
            query_list.append(reservation.serializer())
        print(query_list)
        return JsonResponse(query_list, safe=False)

    def get_queryset(self, params):
        return Reserve.objects.filter(schedule__date=params[0], element__name__icontains=params[1], element__code=params[2])
