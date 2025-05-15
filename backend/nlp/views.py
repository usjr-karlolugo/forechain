from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .serializers import AlertSerializer
import requests


class AlertView(APIView):
    def get(self, request):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictView(APIView):
    def post(self, request):
        title = request.data.get("title", "")
        topic = request.data.get("topic", "")
        sentiment = request.data.get("sentiment", "")

        prompt = f"""
        Analyze this alert and predict its possible impact on the Philippine supply chain:
        Title: {title}
        Topic: {topic}
        Sentiment: {sentiment}
        """

        headers = {
            "Authorization": f"sk-97fbd74b67d643eca71c1988a06660d7",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            result = response.json()
            prediction = result["choices"][0]["message"]["content"].strip()
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
