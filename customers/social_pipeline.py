from django.contrib.auth import login


def login_user(backend, user, response, *args, **kwargs):
    request = backend.strategy.request
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user.is_active = True
    login(request, user)
