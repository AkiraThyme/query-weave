SECRET_KEY = "test-key"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "tests.testapp",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
QUERYWEAVE = {
    "SLOW_QUERY_THRESHOLD_MS": 0,
    "DEBUG_SQL": False,
}
