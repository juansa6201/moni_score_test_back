from __future__ import annotations

from django.core.validators import RegexValidator
from django.db import models

from shared.models import BaseModel
from shared.utils import DNI_REGEX


class Persona(BaseModel):
    class Genero(models.TextChoices):
        HOMBRE = 'M', 'Masculino'
        MUJER = 'F', 'Femenino'
        DESCONOCIDO = 'D', 'Desconocido'

    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(
        max_length=8,
        blank=True,
        validators=[
            RegexValidator(DNI_REGEX, message='%(value)r no es un DNI válido.'),
        ],
    )
    email = models.EmailField(help_text='Email de contacto.')
    genero = models.CharField(max_length=1, choices=Genero.choices, default=Genero.DESCONOCIDO)

    class Meta:
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.dni}'


class Score(BaseModel):
    class Status(models.IntegerChoices):
        RECHAZADO = 0, 'Rechazado'
        APROBADO = 1, 'Aprobado'

    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, related_name='scores')
    status = models.IntegerField(choices=Status.choices)

    class Meta:
        verbose_name_plural = 'Scores'

    def __str__(self):
        return f'{self.persona.dni} - Status: {self.get_status_display()}'
