from __future__ import annotations

from unittest.mock import Mock

import pytest

from scoring.models import Persona
from scoring.models import Score


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def patch_is_client_approved(monkeypatch: pytest.MonkeyPatch):
    mock = Mock(return_value=True)
    monkeypatch.setattr('scoring.serializers.is_client_approved', mock)
    yield mock


@pytest.fixture
def persona() -> Persona:
    persona = Persona(
        nombre='Juan Cruz',
        apellido='Mare',
        dni='12345678',
        email='jcmare18@gmail.com',
        genero=Persona.Genero.DESCONOCIDO,
    )
    persona.save()
    return persona


@pytest.fixture
def score(persona) -> Score:
    score = Score(persona=persona, status=Score.Status.APROBADO)
    score.save()
    return score
