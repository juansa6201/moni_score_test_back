from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http.response import Http404
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.exceptions import APIException as _APIException
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('moni_score')


class APIException(_APIException):
    def __init__(
        self,
        detail: str | list[str] | dict[str, Any] | None = 'Ocurrió un error en el servidor',
        code: str | None = 'error',
        status: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status
        self.extra = extra
        super().__init__(detail, code)


def error_handler(exc: Exception, context: Any) -> Response | None:
    match exc:
        case APIException():
            pass
        case DRFValidationError():
            if isinstance(exc.detail, dict) and exc.detail.get('non_field_errors'):
                exc.detail |= {'detail': '. '.join(exc.detail.pop('non_field_errors'))}
            exc = APIException(exc.detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case DjangoValidationError():
            exc = APIException(exc.message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case RequestException() as e:
            exc = APIException(
                'Error al conectarse con el servicio externo',
                extra={
                    'from': e,
                },
            )
        case Http404():
            exc = APIException('Objeto no encontrado', status=status.HTTP_404_NOT_FOUND)
        case unknown_exc:
            exc = APIException(
                extra={
                    'from': unknown_exc,
                }
            )

    if isinstance(exc, APIException):
        detail = deepcopy(exc.detail)
        logger.exception(detail, extra=exc.extra)

    return exception_handler(exc, context)
