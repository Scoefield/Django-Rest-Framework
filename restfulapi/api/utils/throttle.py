# -*- coding: utf-8 -*-
"""
# @Author: Vino
# @Filename: throttle.py
# @Datetime: 2019/1/13 17:51
"""
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time

VISIT_RECORD = {}

'''
class VisitThrottle(BaseThrottle):
    """
    访问频率控制类（节流）
    10s内只能被访问3次
    """

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """通过用户IP控制访问频率"""
        # 1.获取用户IP
        # remote_addr = request.META.get('REMOTE_ADDR')
        remote_addr = self.get_ident(request)
        
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 10:
            history.pop()

        if len(history) < 3:
            history.insert(0, ctime)
            return True

        # return True     # 表示可以继续访问
        # return False  # 表示访问频率太高，被限制

    def wait(self):
        """
        还需等多少秒才可以访问
        :return:
        """
        ctime = time.time()
        return 10 - (ctime - self.history[-1])
'''


class VisitThrottle(SimpleRateThrottle):
    scope = 'dys'

    def get_cache_key(self, request, view):
        """通过用户IP控制访问频率"""
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = 'user_dys'

    def get_cache_key(self, request, view):
        """通过用户名控制访问频率"""
        return request.user.username
