#!/bin/sh
# python manage.py wait_for_db
python manage.py collectstatic --noinput
# python manage.py migrate --fake
exec gunicorn linapi.wsgi --bind 0.0.0.0:8001
# exec python ./manage.py runserver 0.0.0.0:8001