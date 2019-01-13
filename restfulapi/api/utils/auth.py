# -*- coding: utf-8 -*-
"""
# @Author: Vino
# @Filename: auth.py
# @Datetime: 2019/1/12 20:02
"""
from rest_framework import exceptions
from api import models
from rest_framework.authentication import BaseAuthentication


class FirstAuthtication(BaseAuthentication):
    """
    用户token认证
    """
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass


class Authtication(BaseAuthentication):
    """
    用户token认证
    """
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败！')
        # 在rest framework内部会将这两个字段赋值给request，以供后续使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        return 'Basic realm="api"'
