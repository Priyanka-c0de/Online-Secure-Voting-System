 """
 Django settings for voting project.
 """

 import os
 from pathlib import Path

 BASE_DIR = Path(__file__).resolve().parent.parent

 # -------------------------
 # Security
 # -------------------------

 SECRET_KEY = os.environ.get(
     "SECRET_KEY",
     "django-insecure-n@dc4$jy57^s_3^&#-f_g(98()_phy)6o2k#7lrw&it)v1s$aq"
 )

 DEBUG = os.environ.get("DEBUG", "True") == "True"

 ALLOWED_HOSTS = [
     ".onrender.com",
     "127.0.0.1",
     "localhost",
 ]

 # -------------------------
 # Installed Apps
 # -------------------------

 INSTALLED_APPS = [
     "landing",

     "django.contrib.admin",
     "django.contrib.auth",
     "django.contrib.contenttypes",
     "django.contrib.sessions",
     "django.contrib.messages",
     "django.contrib.staticfiles",
 ]

 # -------------------------
 # Middleware
 # -------------------------

 MIDDLEWARE = [
     "django.middleware.security.SecurityMiddleware",

     "django.contrib.sessions.middleware.SessionMiddleware",
     "django.middleware.common.CommonMiddleware",
     "django.middleware.csrf.CsrfViewMiddleware",
     "django.contrib.auth.middleware.AuthenticationMiddleware",
     "django.contrib.messages.middleware.MessageMiddleware",
     "django.middleware.clickjacking.XFrameOptionsMiddleware",
 ]

 ROOT_URLCONF = "voting.urls"

 # -------------------------
 # Templates
 # -------------------------

 TEMPLATES = [
     {
         "BACKEND": "django.template.backends.django.DjangoTemplates",
         "DIRS": [],
         "APP_DIRS": True,
         "OPTIONS": {
             "context_processors": [
                 "django.template.context_processors.request",
                 "django.contrib.auth.context_processors.auth",
                 "django.contrib.messages.context_processors.messages",
             ],
         },
     },
 ]

 WSGI_APPLICATION = "voting.wsgi.application"

 # -------------------------
 # Database
 # -------------------------

 DATABASES = {
     "default": {
         "ENGINE": "django.db.backends.sqlite3",
         "NAME": BASE_DIR / "db.sqlite3",
     }
 }

 # -------------------------
 # Password Validation
 # -------------------------

 AUTH_PASSWORD_VALIDATORS = [
     {
         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
     },
     {
         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     },
     {
         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
     },
     {
         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
     },
 ]

 # -------------------------
 # Internationalization
 # -------------------------

 LANGUAGE_CODE = "en-us"

 TIME_ZONE = "UTC"

 USE_I18N = True

 USE_TZ = True

 # -------------------------
 # Static & Media Files
 # -------------------------

 STATIC_URL = "static/"
 STATIC_ROOT = BASE_DIR / "staticfiles"

 MEDIA_URL = "/media/"
 MEDIA_ROOT = BASE_DIR / "media"

 # -------------------------
 # Default Primary Key
 # -------------------------

 DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"