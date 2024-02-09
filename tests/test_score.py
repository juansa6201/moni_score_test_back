from __future__ import annotations

from typing import Any

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from scoring.models import Persona
from scoring.models import Score
from scoring.serializers import ScorePOSTSerializer
from scoring.serializers import ScoreSerializer


@pytest.mark.usefixtures(
    'patch_is_client_approved',
)
def test_score_viewset_create():
    data = {
        'nombre': 'Juan Cruz',
        'apellido': 'Mare',
        'dni': '43232227',
        'email': 'jcmare18@gmail.com',
        'genero': 'D',
    }

    client = APIClient()
    res = client.post('/api/score/', data=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert Persona.objects.count() == 1
    body: dict[str, Any] = res.json()  # type: ignore
    assert body == {
        'persona': {
            'nombre': 'Juan Cruz',
            'apellido': 'Mare',
            'dni': '43232227',
            'email': 'jcmare18@gmail.com',
            'genero': 'D',
        },
        'status': 'Aprobado',
    }


@pytest.mark.usefixtures(
    'patch_is_client_approved',
)
def test_score_viewset_create_error():
    data = {
        'nombre': 'Juan Cruz',
        'apellido': 'Mare',
        'dni': '4323222712',
        'email': 'jcmare18',
        'genero': 'D',
    }

    client = APIClient()
    res = client.post('/api/score/', data=data)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert Persona.objects.count() == 0
    body: dict[str, Any] = res.json()  # type: ignore
    assert body['dni'][1] == 'Asegúrese de que este campo no tenga más de 8 caracteres.'
    assert body['email'][0] == 'Introduzca una dirección de correo electrónico válida.'


def test_score_viewset_list(score: Score):
    client = APIClient()
    res = client.get('/api/score/')
    assert res.status_code == status.HTTP_200_OK
    assert Score.objects.count() == 1
    body: dict[str, Any] = res.json()  # type: ignore
    assert body['results'] == [
        {
            'persona': {
                'nombre': 'Juan Cruz',
                'apellido': 'Mare',
                'dni': '12345678',
                'email': 'jcmare18@gmail.com',
                'genero': 'D',
            },
            'status': 'Aprobado',
        }
    ]


def test_score_viewset_update(score: Score):
    data = {
        'nombre': 'Juan Cruz',
        'apellido': 'Mare',
        'dni': '43232227',
        'email': 'jcmare18@gmail.com',
        'genero': 'D',
    }
    client = APIClient()
    res = client.put(f'/api/score/{score.pk}/', data=data)
    assert res.status_code == status.HTTP_200_OK
    assert Score.objects.count() == 1
    body: dict[str, Any] = res.json()  # type: ignore
    assert body == {
        'persona': {
            'nombre': 'Juan Cruz',
            'apellido': 'Mare',
            'dni': '43232227',
            'email': 'jcmare18@gmail.com',
            'genero': 'D',
        },
        'status': 'Aprobado',
    }


def test_score_viewset_delete(score: Score):
    client = APIClient()
    res = client.delete(f'/api/score/{score.pk}/')
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert Score.objects.count() == 0


def test_score_serializer():
    serializer = ScoreSerializer(
        data={
            'persona': {
                'nombre': 'Juan Cruz',
                'apellido': 'Mare',
                'dni': '43232227',
                'email': 'jcmare18@gmail.com',
                'genero': 'D',
            },
            'status': 'Aprobado',
        }
    )
    assert serializer.is_valid(), serializer.errors


def test_score_serializer_errors():
    serializer = ScoreSerializer(
        data={
            'persona': {
                'nombre': 'Juan Cruz',
                'apellido': 'Mare',
                'dni': '4323222723',
                'email': 'jcmare18@gmail.com',
                'genero': 'J',
            },
            'status': 'Aprobado',
        }
    )
    assert not serializer.is_valid()
    assert (
        serializer.errors['persona']['dni'][1]
        == 'Asegúrese de que este campo no tenga más de 8 caracteres.'
    )
    assert serializer.errors['persona']['genero'][0] == '"J" no es una elección válida.'


@pytest.mark.usefixtures(
    'patch_is_client_approved',
)
def test_score_post_serializer(persona: Persona):
    serializer = ScorePOSTSerializer(data={'persona': persona.pk})
    assert serializer.is_valid(), serializer.errors
    score = serializer.save()
    assert Score.objects.count() == 1
    assert Persona.objects.count() == 1
    assert score.get_status_display() == 'Aprobado'
    assert score.persona.nombre == 'Juan Cruz'


def test_score_post_serializer_error():
    serializer = ScorePOSTSerializer(
        data={
            'persona': {
                'nombre': 'Juan Cruz',
                'apellido': 'Mare',
                'dni': '4323222723',
                'email': 'jcmare18@gmail.com',
                'genero': 'J',
            }
        }
    )
    assert not serializer.is_valid(), serializer.errors
    assert Score.objects.count() == 0
    assert Persona.objects.count() == 0
    assert (
        serializer.errors['persona'][0]
        == 'Tipo incorrecto. Se esperaba valor de clave primaria y se recibió dict.'
    )
