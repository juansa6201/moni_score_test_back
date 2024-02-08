from __future__ import annotations

from django.http import JsonResponse
from django.views.generic import TemplateView


async def index(request):
    return JsonResponse({'hello': 'world'})


swagger_ui = TemplateView.as_view(
    template_name='swagger-ui.html',
    extra_context={'schema_url': 'openapi'},
)
