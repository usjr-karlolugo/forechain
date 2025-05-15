from django.db import models
from rest_framework import serializers, generics
from django.urls import path
from django.utils import timezone


# models.py
class Alert(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    sentiment = models.CharField(max_length=50)
    sentiment_score = models.FloatField()
    entities = models.JSONField()  # Store entities in JSON format
    topic = models.CharField(max_length=255, null=True, blank=True)
    score = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# serializers.py
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"


# views.py
class AlertCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


# urls.py
urlpatterns = [
    path("api/alerts/", AlertCreateView.as_view(), name="alert-list-create"),
]
