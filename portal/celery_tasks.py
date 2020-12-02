from portal.celery import app

from libs.wx_message import ApiExceptionRobot, InfoRobot


@app.task()
def notify_exception_message(content):
    ApiExceptionRobot().send_text(content)


@app.task()
def business_info(content):
    InfoRobot().send_text(content)
