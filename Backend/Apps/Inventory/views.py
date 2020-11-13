from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import InventorySerializer


class InventoryListApi(generics.ListAPIView):
   # permission_classes = (IsAuthenticated,)
    serializer_class = InventorySerializer
    model = Inventory

    def get_queryset(self):
        return Inventory.objects.filter(code__icontains=self.request.GET["code"]).order_by("code")

