# coding=utf-8
import os
import sys
from sae.const import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB, MYSQL_HOST_S

# 重载字符集
reload(sys)
sys.setdefaultencoding('utf8')

IN_SAE = 'SERVER_SOFTWARE' in os.environ  # 是否在SAE引擎上运行

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST_S,
        'PORT': MYSQL_PORT,
        'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        'TIMEOUT': 86400,
        'VERSION': 1,
    }
}

LANGUAGE_CODE = 'zh-cn'

USE_I18N = False  # 关闭多语言引擎，优化性能

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False  # 不开启时区，如开启，数据库字段将会保存为UTC时间，而不是本地时间

STATIC_URL = '/static/'


# patchers

def patch_disable_fetchurl():
    """ 禁用掉fetchurl服务， 使用socket服务来处理请求，如此一来，可进行follow操作（如果用fetchurl服务，则无法进行follow操作）
        请参见：http://sae.sina.com.cn/?m=devcenter&catId=291
    """
    os.environ['disable_fetchurl'] = '1'


def patch_http_host(http_host='localhost'):
    """ 设置环境变量HTTP_HOST，本地测试TaskQueue时需要该变量，仅用于本地测试
    """
    os.environ.setdefault('HTTP_HOST', http_host)


def patch_pylibmc():
    """ 伪装pylibmc模块，仅用于本地测试
    """
    import sae.memcache

    sys.modules['pylibmc'] = sae.memcache


def patch_sae_restful_mysql():
    from sae._restful_mysql import monkey

    monkey.patch()


def get_database(name, user, password, host=MYSQL_HOST, port=MYSQL_PORT, alias='default',
                 engine='django.db.backends.mysql', **options):
    options.setdefault('init_command', "SET storage_engine=MYISAM;")
    return {
        alias: {
            'ENGINE': engine,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
            'OPTIONS': options,
        }
    }


if IN_SAE:
    DEBUG = False
    TEMPLATE_DEBUG = False
    DATABASE_ROUTERS = ['django_sae.db.routers.MasterSlaveRouter']  # 读写分离
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    DATABASE_ROUTERS = []

    patch_pylibmc()
    patch_http_host()