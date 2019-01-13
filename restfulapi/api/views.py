from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from api.utils.auth import Authtication, FirstAuthtication
from api.utils.permission import SVIPPermission, MyPermission1
from api.utils.throttle import VisitThrottle
import time
from api import models

ORDER_DICT = {
    1: {
        'name': 'iPhone',
        'price': 6000,
        'count': 350,
        'content': '库克推荐'
    },
    2: {
        'name': '小米',
        'price': 5000,
        'count': 150,
        'content': '雷军推荐'
    }
}


def md5(user):
    """
    根据user和时间戳生成md5
    :param user:
    :return:
    """
    import hashlib
    import time
    ctime = time.time()
    m = hashlib.md5()
    m.update(bytes(user, encoding='utf-8'))
    token = m.hexdigest() + str(int(ctime))
    # print(token)
    return token


class AuthView(APIView):
    """
    用户登录认证
    """
    authentication_classes = []  # 空列表表示无须进行token认证（一开始没有登录，无需token认证）
    permission_classes = []     # 无须进行权限认证
    throttle_classes = [VisitThrottle, ]    # 通过IP控制访问频率

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            # print(user, pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建token，利用md5(用户名)+当前时间戳
            token = md5(user)
            # 登录成功后，token存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


class OrderView(APIView):
    """
    订单相关业务（假设只有SVIP有权限）
    """

    # authentication_classes = [Authtication, ]   # 使用token认证
    # permission_classes = [SVIPPermission, ]   # 权限认证类对象

    def get(self, request, *args, **kwargs):
        # request.user
        # request.auth
        self.dispatch
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
            # ret['code'] = 1002
            # ret['msg'] = '请求异常'
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    用户信息相关业务（普通用户、VIP）
    """

    permission_classes = [MyPermission1, ]  # 权限认证类对象

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None, 'data': None}
        uinfo = {}
        try:
            ret['msg'] = '请求成功'
            uinfo['username'] = request.user.username
            uinfo['password'] = request.user.password
            uinfo['user_type'] = request.user.user_type
            uinfo['token'] = request.auth.token
            ret['data'] = uinfo
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)
