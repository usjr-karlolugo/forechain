from django.urls import path
from .views import AlertView

urlpatterns = [
    path("api/alerts", AlertView.as_view(), name="alert"),
]
