#!/bin/sh
gunicorn -c gunicorn_settings.py wsgi:app
# flask db init
# flask db migrate
# flask db upgrade
# python3 entrypoint.py
# /bin/bash