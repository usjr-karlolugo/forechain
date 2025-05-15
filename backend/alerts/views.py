from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import AlertSerializer
from rest_framework import generics
from .models import Alert


class AlertView(APIView):
    def get(self, request):
        # Fetch all alerts from the database
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.all().order_by("-created_at")  # most recent first
    serializer_class = AlertSerializer
