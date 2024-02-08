from __future__ import annotations

from config.settings import *  # noqa: F403

INSTALLED_APPS += ['tests']  # noqa: F405

DATABASES |= {'default': dj_database_url.parse('sqlite://:memory:')}  # noqa: F405
