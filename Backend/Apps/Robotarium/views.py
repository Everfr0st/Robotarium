from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.Robotarium.models import Robot
from Apps.Robotarium.serializer import RobotSerializer


class RobotsListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RobotSerializer
    model = Robot
    queryset = model.objects.all().order_by("-name")


class RobotUpdateAvailableStatusApi(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        status = request.data["status"]
        print(status, "sd")
        robot = Robot.objects.filter(name=request.data["robot"]).first()
        if robot:
            robot.available = status
            robot.save()
            return Response({
                "Detail": "Robot status updated",
                "status": robot.available
            }, status=200)
        else:
            return Response({"Detail": "Robot not found"}, status=404)
