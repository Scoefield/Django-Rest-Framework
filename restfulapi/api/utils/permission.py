# -*- coding: utf-8 -*-
"""
# @Author: Vino
# @Filename: permission.py
# @Datetime: 2019/1/13 12:58
"""


class MyPermission(object):
    """
    权限认证类
    """

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPermission1(object):
    """
    权限认证类
    """

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
