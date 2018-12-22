import time

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from FasterRunner.settings import INVALID_TIME
from fastuser import models


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):
        # 前面request.query_params是获取查询字符串参数，后面加个.dict()  没看懂，就自己实验了一下
        # request.query_params
        # 这个获取的类型是
        # django里面的 QueryDict
        # 类型，后面加.dict()
        # 是转变成
        # python中字典格式。
        token = request.query_params.get("token", None)
        obj = models.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed({
                "code": "9998",
                "msg": "用户未认证",
                "success": False
            })

        update_time = int(obj.update_time.timestamp())
        current_time = int(time.time())

        if current_time - update_time >= INVALID_TIME:
            raise exceptions.AuthenticationFailed({
                "code": "9997",
                "msg": "登陆超时，请重新登陆",
                "success": False
            })

        # valid update valid time
        obj.token = token
        obj.save()
        # 发送到数据库

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'
