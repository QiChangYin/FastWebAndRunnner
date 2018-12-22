from rest_framework.response import Response
from rest_framework.views import APIView
from fastuser.common import response
from fastuser import models
from fastuser import serializers
import logging
# Create your views here.
from fastuser.common.token import generate_token
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
# ObjectDoesNotExistfrom django.core
logger = logging.getLogger('FastRunner')


class RegisterView(APIView):

    authentication_classes = ()
    permission_classes = ()
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    """
    注册:{
        "user": "demo"
        "password": "1321"
        "email": "1@1.com"
    }
    """

    def post(self, request):

        try:
            username = request.data["username"]
            password = request.data["password"]
            email = request.data["email"]
        except KeyError:
            return Response(response.KEY_MISS)

        if models.UserInfo.objects.filter(username=username).first():
            return Response(response.REGISTER_USERNAME_EXIST)

        if models.UserInfo.objects.filter(email=email).first():
            return Response(response.REGISTER_EMAIL_EXIST)

        # 此处采用django自带的方法来加密
        request.data["password"] = make_password(password)

        print(type(request.data["password"]))
        serializer = serializers.UserInfoSerializer(data=request.data)
        print(type(serializer))
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(response.REGISTER_SUCCESS)
        else:
            return Response(response.SYSTEM_ERROR)


class LoginView(APIView):
    """
    登陆视图，用户名与密码匹配返回token
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        用户名密码一致返回token
        {
            username: str
            password: str
        }
        """
        try:
            username = request.data["username"]
            password = request.data["password"]

        # 此处的高明出在捕获keyError不存在的时候,那么就是搓蛋
        except KeyError:
            return Response(response.KEY_MISS)

        user = models.UserInfo.objects.filter(username=username).first()

        if not user:
            return Response(response.USER_NOT_EXISTS)

        if not check_password(password, user.password):
            return Response(response.LOGIN_FAILED)

        token = generate_token(username)
        print(token)
        try:
            models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
        # 此处的意义很重大的,可以捕获对象不存在的错误
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)
        else:
            response.LOGIN_SUCCESS["token"] = token
            response.LOGIN_SUCCESS["user"] = username
            return Response(response.LOGIN_SUCCESS)


