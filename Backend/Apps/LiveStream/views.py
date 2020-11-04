from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import LiveStreamId
class RetrieveLivestreamId(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        live_id = LiveStreamId.objects.all()

        if live_id.exists():
            live_id = live_id[0].live_id
        else:
            live_id = ""
        return JsonResponse({'live_id': live_id})
        

