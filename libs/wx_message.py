"""
20200226
企业微信通知
"""
from datetime import datetime
import requests
import hashlib
import base64
import socket

from portal.settings import DEBUG, ENV


WX_ROBOT_API_EXCEPTION = None
WX_ROBOT_INFO = None

# 日志这样
# > [环境 PRODUCTION / SANDBOX]
# > [来源 AppName - Module / Service]
# > [类型 WARN / DEBUG / INFO / ERROR ]
# > [ip (如果有) ]
# > [时间]
# [事件：主角，行为，对象]


class BaseRobot:
    robot_url = ''
    message_level = 'EXCEPTION'
    receiver = []

    def format_message(self, content, source):
        content = f"> [环境 {ENV}]\n" \
                  f"> [主机 {socket.gethostname()}]\n" \
                  f"> [来源 {source}]\n" \
                  f"> [类型 {self.message_level}]\n" \
                  f"> [时间 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n" \
                  f"{content}"
        return content

    def send_text(self, content, source=None):
        """
        推送消息到企业微信机器人
        :param content: 消息
        :param source: 来源
        :return:
        """
        if source is None:
            source = type(self).__name__

        content = self.format_message(content, source)
        if DEBUG:
            print(content)
            return
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_mobile_list": self.receiver
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        requests.post(self.robot_url, json=data, headers=headers, timeout=5)

    def send_image_from_bs64(self, base64_, md5):
        """
        推送图片到企业微信机器人
        :param base64_:
        :param md5:
        :return:
        """
        if DEBUG:
            print('send img')
            return
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64_,
                "md5": md5
            }
        }
        requests.post(url=self.robot_url, json=data, timeout=5)

    def send_img(self, path):
        """
        :param path: 图片位置
        :return:
        """
        with open(path, 'rb') as f:
            data = f.read()
            base64_ = base64.b64encode(data).decode('utf-8')
            m = hashlib.md5(data)
            md5 = m.hexdigest()
            self.send_image_from_bs64(base64_, md5)


class ApiExceptionRobot(BaseRobot):
    """
    api 报错
    """
    robot_url = WX_ROBOT_API_EXCEPTION
    message_level = 'EXCEPTION'
    receiver = []

    def __init__(self):
        super().__init__()


class InfoRobot(BaseRobot):
    """
    业务通知
    """
    robot_url = WX_ROBOT_INFO
    message_level = 'INFO'
    receiver = []

    def __init__(self):
        super().__init__()