# coding=utf-8
import os


def patch_http_host(http_host='localhost'):
    """ 设置本地TaskQueue测试时需要的参数，否则test时client会出错，用于本地测试
    """
    os.environ.setdefault('HTTP_HOST', http_host)


def patch_disable_fetchurl():
    """ 禁用掉fetchurl服务， 使用socket服务来处理请求，如此一来，可进行follow操作（如果用fetchurl服务，则无法进行follow操作）
        参见：http://sae.sina.com.cn/?m=devcenter&catId=291
    """
    os.environ['disable_fetchurl'] = '1'