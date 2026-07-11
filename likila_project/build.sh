#!/usr/bin/env bash
# Render runs this on every deploy
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed   # only adds missing data, safe to run on every deploy
