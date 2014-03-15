# coding=utf-8
import os


def patch_http_host(http_host='localhost'):
    """ 设置本地TaskQueue测试时需要的参数，否则test时client会出错，用于本地测试
    """
    os.environ.setdefault('HTTP_HOST', http_host)