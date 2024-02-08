from __future__ import annotations

import logging
from collections import OrderedDict
from typing import Any

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers as s

from moni_client.service import is_client_approved
from scoring import models

logger = logging.getLogger('scoring.serializers')


class PersonaSerializer(s.ModelSerializer[models.Persona]):
    """Serializer para el modelo Persona."""

    class Meta:
        model = models.Persona
        fields = (
            'nombre',
            'apellido',
            'dni',
            'email',
            'genero',
        )


class ScoreSerializer(s.ModelSerializer[models.Score]):
    """Serializer para el modelo Score."""

    persona = PersonaSerializer()
    status = s.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = models.Score
        fields = (
            'persona',
            'status',
        )


@extend_schema_serializer(exclude_fields=('status',))
class ScorePOSTSerializer(s.ModelSerializer[models.Score]):
    """Serializer para la creación de un nuevo Score."""

    def validate(self, data: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """Valida y procesa los datos antes de guardar."""
        persona: models.Persona = data['persona']
        # Obtiene si el cliente esta habilitado o no para pedir un prestamo y le asigna el estado a la clave 'status'.
        data['status'] = is_client_approved(persona.dni)
        return data

    class Meta:
        model = models.Score
        fields = ('persona',)
