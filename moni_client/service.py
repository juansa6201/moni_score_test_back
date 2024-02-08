from __future__ import annotations

import json
from typing import Final

import requests
from rest_framework import status

from config.settings import MONI_TOKEN
from config.settings import MONI_URL
from shared.exceptions import APIException

MONI_REQUEST_TIMEOUT: Final[tuple[int, int]] = (5, 5)


class Session(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', MONI_REQUEST_TIMEOUT)
        kwargs['headers'] = {'credential': MONI_TOKEN}
        return super().request(*args, **kwargs)


session = Session()


def is_client_approved(dni: str) -> bool:
    url = f'{MONI_URL}/{dni}'
    try:
        res = session.get(url)
    except requests.exceptions.RequestException as e:
        raise APIException(
            'Error al conectarse con un servicio externo.',
            extra={
                'from': e,
            },
        )
    if res.status_code != status.HTTP_200_OK:
        raise APIException(
            f'No se pudo obtener informacion del servicio externo. HTTP Status: {res.status_code}'
        )
    try:
        body = res.json()
    except json.JSONDecodeError:
        raise APIException('No se pudo decodear la respuesta del servicio externo.')

    if body['status'] != 'approve':
        return False
    return True
