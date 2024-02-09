from __future__ import annotations

from scoring.models import Persona
from scoring.serializers import PersonaSerializer


def test_persona_serializer():
    serializer = PersonaSerializer(
        data={
            'nombre': 'Juan Cruz',
            'apellido': 'Mare',
            'dni': '43232227',
            'email': 'jcmare18@gmail.com',
            'genero': 'D',
        }
    )
    assert serializer.is_valid(), serializer.errors

    persona = serializer.save()
    assert Persona.objects.count() == 1
    assert persona.nombre == 'Juan Cruz'


def test_persona_serializer_error():
    serializer = PersonaSerializer(
        data={
            'nombre': 'Juan Cruz',
            'apellido': 'Mare',
            'dni': '4323222723',
            'email': 'jcmare18@gmail.com',
            'genero': 'Z',
        }
    )
    assert not serializer.is_valid()
    assert (
        serializer.errors['dni'][1] == 'Asegúrese de que este campo no tenga más de 8 caracteres.'
    )
    assert serializer.errors['genero'][0] == '"Z" no es una elección válida.'
    assert Persona.objects.count() == 0
