web: python manage.py runserver 0.0.0.0:$PORT
release: python manage.py migrate
worker: celery worker --app=tasks.app
REDIS_URL=rediss://:p935eb5f0097da33d3517959945c79180f38c8a05ea62bdac9c4e82bf405e51e5@ec2-52-71-63-156.compute-1.amazonaws.com:13730
