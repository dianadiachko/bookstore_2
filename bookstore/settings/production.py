from .base import *

DEBUG = False
ALLOWED_HOSTS = ["your-domain.com"]

MIDDLEWARE.insert(
    1,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"