import os

# Configure the domain name using the environment variable that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 'agronomy.live', 'www.agronomy.live'] if os.environ['PRODUCTION'] == 'Yes' else []
ALLOWED_DOMAIN = ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME'], 'https://agronomy.live', 'https://www.agronomy.live'] if os.environ['PRODUCTION'] == 'Yes' else []

# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'Agronomy.middleware.WwwRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Agronomy.middleware.SessionCheckerMiddleware',
    'Agronomy.middleware.PreventGoogleOauthMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SESSION_COOKIE_SECURE = True
