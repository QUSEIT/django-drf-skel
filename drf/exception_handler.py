import traceback

from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback

from drf.exception import ApiException, AuthException, DsApiException
from drf.response import ApiResponse
from portal.celery_tasks import notify_exception_message
from portal.settings import DEBUG


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    path = context['request'].path
    if path.startswith('/api/out'):
        return open_api_exception_handler(exc, context)
    else:
        return app_api_exception_handler(exc, context)


def app_api_exception_handler(exc, context):
    """
    supplier app api 异常处理
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.AuthenticationFailed):
        # shopify 登陆
        return Response(
            {
                'errorno': 2,
                'message': "Please login.",
                'redirect_url': '/login'}
        )

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'message': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    if isinstance(exc, ApiException):
        # 处理抛出的业务错误
        detail = exc.detail
        return ApiResponse(errno=1, msg=detail)

    if isinstance(exc, Exception):
        # 处理异常
        if DEBUG is False:
            content = traceback.format_exc()
            notify_exception_message.delay(content)
            return ApiResponse(errno=2, msg='Server Error!')
        else:
            raise exc
    return None


def open_api_exception_handler(exc, context):
    """
    ds app api 异常处理
    {
        "data": {}
        "code": http status code,
        "status": "success",
        "message": "OK"
    }
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.AuthenticationFailed):
        return Response({
                'code': 401,
                'status': "fail",
                'message': 'Please login.'})

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        set_rollback()
        return Response({
            'code': exc.status_code,
            'status': "fail",
            'message': exc.detail
        })

    if isinstance(exc, ApiException):
        # supplier app 异常处理
        detail = exc.detail
        return Response({
            'code': 400,
            'status': "fail",
            'message': detail
        })

    if isinstance(exc, DsApiException):
        # ds app api 异常
        detail = exc.detail
        return Response({
            "code": 500,
            "status": "fail",
            "message": detail})

    if isinstance(exc, Exception):
        # 处理异常
        if DEBUG is False:
            content = traceback.format_exc()
            notify_exception_message.delay(content)
            return Response({
                'code': 500,
                'status': "fail",
                'message': 'Server error'
            })
        else:
            raise exc
    return None
