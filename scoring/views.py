from __future__ import annotations

from typing import Any

import django_filters.rest_framework as django_filters
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from scoring import models
from scoring import serializers
from scoring.filters import ScoreFilter
from shared import pagination

# Definición de la vista ScoreViewSet.


@extend_schema(tags=['Score'])
class ScoreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    # No definimos el update porque agrega el metodo PATCH que no necesitamos.
    viewsets.GenericViewSet,
):
    queryset = models.Score.objects.all().order_by('id').order_by('-created_at')
    serializer_class = serializers.ScoreSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = ScoreFilter

    @extend_schema(
        request=serializers.PersonaPOSTSerializer,
        responses={status.HTTP_201_CREATED: serializer_class},
        examples=[
            OpenApiExample(
                name='persona',
                request_only=True,
                value={
                    'nombre': 'Juan Cruz',
                    'apellido': 'Mare',
                    'dni': '43232525',
                    'email': 'test@gmail.com',
                    'genero': 'M',
                },
            ),
        ],
    )
    # Definición del método para crear un nuevo objeto Score.
    def create(self, request: Request, *args, **kwargs) -> Response:
        # Serializa, valida y guarda la persona a crear.
        persona_serializer = serializers.PersonaPOSTSerializer(data=request.data)
        persona_serializer.is_valid(raise_exception=True)
        persona: models.Persona = persona_serializer.save()

        # Serializa, valida y guarda el score a crear.
        socre_serializer = serializers.ScorePOSTSerializer(data={'persona': persona.pk})
        socre_serializer.is_valid(raise_exception=True)
        score = socre_serializer.save()

        # Serializa la respuesta y se retorna un Response con el objeto creado y el status 201.
        res_serializer = self.serializer_class(score)
        headers = self.get_success_headers(res_serializer.data)
        return Response(res_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        request=serializers.PersonaPOSTSerializer,
        responses={status.HTTP_200_OK: serializer_class},
        examples=[
            OpenApiExample(
                name='persona',
                request_only=True,
                value={
                    'nombre': 'Juan Cruz',
                    'apellido': 'Mare',
                    'dni': '43232525',
                    'email': 'test@gmail.com',
                    'genero': 'M',
                },
            ),
        ],
    )
    # Definición del método para actualizar un objeto Score.
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # Obtiene la instancia Score.
        instance = self.get_object()

        # Serializa, valida y guarda la persona a actualizar.
        persona_serializer = serializers.PersonaPOSTSerializer(
            instance=instance.persona, data=request.data
        )
        persona_serializer.is_valid(raise_exception=True)
        persona_serializer.save()

        # Serializa la instancia Score con la persona actualizada.
        serializer = serializers.ScoreSerializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
