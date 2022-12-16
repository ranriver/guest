# _*_ coding: utf-8 _*_
# @Time: 2022/12/16 16:57
# @Author: river
# @File: uwsgi_test.py


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]
