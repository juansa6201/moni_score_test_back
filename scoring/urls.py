from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework import routers

from scoring import views

# Define el enrutador de la aplicación.
router = routers.DefaultRouter()
router.root_view_name = 'api'
router.register('scores', views.ScoreViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
