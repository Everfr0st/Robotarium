from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Apps.Robotarium.models import Robot
from Apps.Robotarium.serializer import RobotSerializer


class RobotsListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RobotSerializer
    model = Robot
    queryset = model.objects.all().order_by("-name")
