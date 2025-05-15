"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from alerts.views import AlertView, AlertCreateView, AlertListView
from nlp.views import PredictView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("alerts/", AlertView.as_view(), name="alert-list"),
    path("api/alerts/", AlertView.as_view(), name="alert-list"),
    path("api/alerts/create/", AlertCreateView.as_view(), name="alert-create"),
    path("api/alerts/list/", AlertListView.as_view(), name="list-alerts"),  # GET
    path("api/predict", PredictView.as_view(), name="predict"),
    path("", include("nlp.urls")),
]
