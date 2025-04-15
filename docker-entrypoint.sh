 #!/bin/bash
set -e

# Source environment variables if .env exists
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn --bind 0.0.0.0:8000 yearfilter.wsgi