#!/bin/sh

echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

python manage.py init_user

exec "$@"

