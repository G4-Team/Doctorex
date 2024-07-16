from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

SECRET_KEY = env("PRODUCTION_SECRET_KEY")

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db" / "db.sqlite3",
    }
}
