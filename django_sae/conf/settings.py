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

LANGUAGE_CODE = 'zh-hans'  # zh-cn从1.7版本后弃用

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


def patch_task_queue(host='localhost', port=8080):
    """ 用于虚拟SAE的TaskQueue服务，仅用于本地开发环境
    """
    os.environ['HTTP_HOST'] = '%s:%d' % (host, port)


def patch_memcache():
    """ 用于虚拟本地开发环境的Memcache服务，数据将保存在内存中
    """
    import sae.memcache

    sys.modules['pylibmc'] = sae.memcache


def patch_kvdb(file_path):
    """ 用于虚拟本地开发环境的KVDB服务，数据将保存到指定的文件中
    """
    os.environ['sae.kvdb.file'] = os.path.abspath(file_path)


def patch_storage(file_path):
    """ 用于虚拟本地开发环境的Storage服务，数据将保存到指定的文件中
    """
    os.environ['sae.storage.path'] = os.path.abspath(file_path)


def patch_app_info(name, version='1'):
    """ 用于虚拟环境变量APP_NAME和APP_VERSION
    """
    os.environ['APP_NAME'] = name
    os.environ['APP_VERSION'] = version


def patch_sae_restful_mysql():
    """ 用于直接操作线上的数据库
    """
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

    patch_memcache()
    patch_task_queue()