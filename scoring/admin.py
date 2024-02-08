from __future__ import annotations

from django.contrib import admin

from . import models


admin.site.disable_action('delete_selected')


@admin.register(models.Persona)
class PersonaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    pass
