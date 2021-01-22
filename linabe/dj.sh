#!/bin/sh
exec python ./manage.py runserver 0.0.0.0:8001

# docker-compose up -d --force-recreate --no-deps --build nginx