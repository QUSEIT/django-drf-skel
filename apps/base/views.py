import os
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf.authentication import is_token_expired
from rest_framework.authentication import get_authorization_header
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from drf.exception import ApiException
from drf.response import ApiResponse
from .serializer import UserSerializer


class AuthView(viewsets.GenericViewSet):
    """
    staff api
    """
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def get_token(request):
        auth = get_authorization_header(request).split()
        token = None
        if auth and auth[0].lower() == 'token'.encode():
            try:
                key = auth[1].decode()
                token = Token.objects.get(key=key)
            except Exception:
                pass
        return token

    @action(detail=False, methods=['GET'])
    def hello(self, request):
        return ApiResponse({'speak': 'hello'})

    @action(detail=False, methods=['get'])
    def captcha(self, request):
        hash_key = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(hash_key)
        return ApiResponse({'captcha': captcha_url, 'hash_key': hash_key})

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        login
        """
        data = request.data
        username = data.get('username')
        password = data.get('password')
        hash_key = data.get('hash_key')
        captcha = data.get('captcha')
        if captcha is None:
            raise ApiException('请填写验证码！')
        if username is None or password is None:
            raise ApiException('请填写用户名密码！')
        if not CaptchaStore.objects.filter(response=captcha,
                                           hashkey=hash_key,
                                           expiration__gte=datetime.now()).exists():
            raise ApiException('无效验证码')
        user = authenticate(request=request,
                            username=username, password=password)
        if not user:
            raise ApiException('无效用户或密码错误！')
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            is_expired = is_token_expired(token)
            if is_expired:
                token.delete()
                token = Token.objects.create(user=user)
        return ApiResponse({"token": token.key}, msg='登陆成功！')

    @action(detail=False, methods=['get'] )
    def check_token(self, request):
        """
        check token
        """
        token = self.get_token(request)
        if token:
            if not is_token_expired(token):
                return ApiResponse({'is_login': True}, msg='有效 token！')
        return ApiResponse({'is_login': False}, msg='无效 token！')

    @action(detail=False, methods=['get'])
    def logout(self, request):
        token = self.get_token(request)
        if token:
            token.delete()
        return ApiResponse({}, msg='退出登陆成功！')
