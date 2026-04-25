SECRET_KEY = "example-key"
DEBUG = True
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "sample_app",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
USE_TZ = True
ROOT_URLCONF = "django_project.urls"
QUERYWEAVE = {
    "SLOW_QUERY_THRESHOLD_MS": 500,
    "DEBUG_SQL": False,
}
