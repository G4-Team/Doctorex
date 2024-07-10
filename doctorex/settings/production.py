from .base import *

DEBUG = False
ALLOWED_HOSTS = []

SECRET_KEY = env("PRODUCTION_SECRET_KEY")

# Database
DATABASES = {"default": env.db("PRODUCTION_DATABASE_URL")}