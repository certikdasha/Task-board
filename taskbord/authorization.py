from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from django.conf import settings
from taskbord.models import CustomToken


class CustomTokenAuth(TokenAuthentication):
    model = CustomToken

    def authenticate(self, request):
        auth = super().authenticate(request=request)
        if auth:
            user, token = auth
            if token.last_action and (timezone.now() - token.last_action).seconds > settings.AUTO_LOGOUT_DELAY * 60:
                msg = 'Token timed out.'
                raise exceptions.AuthenticationFailed(msg)
            token.last_action = timezone.now()
            token.save()
            return user, token
