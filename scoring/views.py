from __future__ import annotations

import django_filters.rest_framework as django_filters
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from scoring import models
from scoring import serializers
from shared import pagination

# Definición de la vista ScoreViewSet.


@extend_schema(tags=['Score'])
class ScoreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Score.objects.all().order_by('id')
    serializer_class = serializers.ScoreSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (django_filters.DjangoFilterBackend,)

    @extend_schema(
        request=serializers.PersonaSerializer,
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
    def create(self, request, *args, **kwargs) -> Response:
        # Se serializa, valida y guarda la persona a crear.
        persona_serializer = serializers.PersonaSerializer(data=request.data)
        persona_serializer.is_valid(raise_exception=True)
        persona: models.Persona = persona_serializer.save()

        # Se serializa, valida y guarda el score a crear.
        socre_serializer = serializers.ScorePOSTSerializer(data={'persona': persona.pk})
        socre_serializer.is_valid(raise_exception=True)
        score = socre_serializer.save()

        # Se serializa la respuesta y se retorna un Response con el objeto creado y el status 201.
        res_serializer = self.serializer_class(score)
        headers = self.get_success_headers(res_serializer.data)
        return Response(res_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
