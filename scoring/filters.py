from __future__ import annotations

import django_filters.rest_framework as django_filters
from django.db.models import QuerySet

from scoring.models import Score


class ScoreFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    dni = django_filters.CharFilter(
        field_name='persona__dni',
        lookup_expr='icontains',
    )
    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method='filter_status',
    )
    sort = django_filters.OrderingFilter(
        fields={
            'id': 'id',
            'created_at': 'created_at',
            'status': 'status',
        }
    )

    def filter_status(self, queryset: QuerySet[Score], name: str, value: str) -> QuerySet:
        match value:
            case 'aprobado':
                return queryset.filter(status=Score.Status.APROBADO)
            case 'rechazado':
                return queryset.filter(status=Score.Status.RECHAZADO)

        return queryset

    class Meta:
        model = Score
        fields = (
            'dni',
            'status',
            'sort',
        )
