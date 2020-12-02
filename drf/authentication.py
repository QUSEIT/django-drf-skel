import json

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from django.middleware.csrf import CsrfViewMiddleware, get_token

from libs.cropty import hmac_validate_token
from drf.exception import AuthException

import hashlib


def is_token_expired(token):
    delta = timezone.now() - token.created
    print(delta.total_seconds(), settings.TOKEN_EXPIRED)
    return delta.total_seconds() > settings.TOKEN_EXPIRED


class ExpiredTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if is_token_expired(token):
            raise exceptions.AuthenticationFailed(_('token is expired.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)


class HmacAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # hmac login os3系统请求os接口
        hmac_token = request.META.get('HTTP_HMAC_TOKEN')
        if hmac_token:
            if request.method == 'POST':
                content = request.body.decode('utf-8')
                is_valid = hmac_validate_token(content[:1000], hmac_token)
            elif request.method == 'GET':
                params = json.dumps(request.GET.dict())
                is_valid = hmac_validate_token(params[:1000], hmac_token)
            else:
                is_valid = False

            if is_valid:
                return ('os3', None)

        raise exceptions.AuthenticationFailed(_('Please login'))


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


