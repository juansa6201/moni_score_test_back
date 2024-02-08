#!/bin/sh
set -xe

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py diffsettings | grep -E '(HOSTS|ORIGINS)'
gunicorn config.asgi:application "$@"
