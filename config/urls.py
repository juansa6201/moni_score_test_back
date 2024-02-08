from __future__ import annotations

from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import URLPattern
from django.urls import URLResolver

from config.settings import URL_PREFIX

urlpatterns: list[URLPattern | URLResolver] = [
    path('admin/', admin.site.urls),
    path('', include('openapi.urls'), name='openapi'),
    path('api/', include('scoring.urls'), name='scoring'),
]

if URL_PREFIX:
    urlpatterns = [
        path(f'{URL_PREFIX}/', include(urlpatterns)),
    ]
