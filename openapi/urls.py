from __future__ import annotations

from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView

from openapi import views

urlpatterns = [
    path('', views.index, name='index'),
    path('openapi.json', SpectacularJSONAPIView.as_view(), name='openapi'),
    path('swagger/', views.swagger_ui, name='swagger'),
]
