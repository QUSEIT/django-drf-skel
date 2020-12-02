from rest_framework.response import Response


class ApiResponse(Response):
    """
    通用返回数据
    """
    def __init__(self, data=None, msg=None, errno=0, status=None, **kwargs):
        msg = msg if msg is not None else ''
        res = data if data is not None else {}
        data = {
            "errorno": errno,
            "data": res,
            "msg": msg,
            **kwargs
        }
        super().__init__(data=data, status=status)


class DsApiResponse(Response):
    """
    通用返回数据
    """
    def __init__(self, data=None, msg=None, status=None, code=200, **kwargs):
        msg = msg if msg is not None else 'OK'
        status = status if status is not None else 'success'
        res = data if data is not None else {}
        data = {
            "code": code,
            "status": status,
            "message": msg,
            "data": res,
            **kwargs
        }
        super().__init__(data=data, status=code)
