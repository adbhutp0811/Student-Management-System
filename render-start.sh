#!/usr/bin/env bash
set -e
python manage.py migrate --noinput
exec gunicorn student_management.wsgi:application --workers 2 --worker-class sync --timeout 120 --access-logfile - --log-level info
