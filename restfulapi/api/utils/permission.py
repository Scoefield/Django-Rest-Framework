# -*- coding: utf-8 -*-
"""
# @Author: Vino
# @Filename: permission.py
# @Datetime: 2019/1/13 12:58
"""
from rest_framework.permissions import BasePermission   # rest_framework内置权限类，按照规范，下面权限认证类一般会继承它


class SVIPPermission(BasePermission):
    """
    权限认证类
    """
    message = "必须是SVIP才能访问"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPermission1(BasePermission):
    """
    权限认证类
    """

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
