from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"  # Or list: ['title', 'content', 'sentiment', 'entities', 'created_at']
