class ApiException(Exception):
    """
    supplier app 业务层面的异常
    """
    def __init__(self, detail=None):
        if detail is None:
            self.detail = 'A server error occurred.'
        else:
            self.detail = detail


class DsApiException(Exception):
    """
    ds app api 异常处理
    """
    def __init__(self, detail=None):
        if detail is None:
            self.detail = 'A server error occurred.'
        else:
            self.detail = detail


class AuthException(Exception):
    """

    """
    def __init__(self, detail=None):
        self.detail = 'Wechat Need login'