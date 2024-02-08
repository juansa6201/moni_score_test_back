from __future__ import annotations

from typing import Any

from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 42,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': f'http://api.example.org/accounts/?{self.page_query_param}=4',
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': f'http://api.example.org/accounts/?{self.page_query_param}=3',
                },
                'results': schema,
            },
            # Cuando no trae results el count es 0 y results es una lista vacía. Según el schema
            # de drf pueden ser null, pero no es el caso.
            'required': ['count', 'results'],
        }
