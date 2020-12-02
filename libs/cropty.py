import time
import hmac
from base64 import b64decode, b64encode

from portal.settings import API_SECRET_KEY


def hmac_encrypt(content):
    """
    :param content:
    :return:
    """
    secret = API_SECRET_KEY.encode('utf-8')
    content_bytes = content.encode('utf-8')
    h = hmac.new(secret, content_bytes, digestmod='SHA1')
    token = h.hexdigest()
    return token


def hmac_generate_token(content):
    token = hmac_encrypt(content)
    return b64encode(token.encode('utf-8')).decode('utf-8')


def hmac_validate_token(content, token):
    cal_token = hmac_encrypt(content)
    cal_token = b64encode(cal_token.encode('utf-8')).decode('utf-8')
    return cal_token == token
