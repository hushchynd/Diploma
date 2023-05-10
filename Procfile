web: python manage.py runserver 0.0.0.0:$PORT
release: python manage.py migrate
worker: celery worker --app=tasks.app
REDIS_URL=redis://127.0.0.1:6379/0
