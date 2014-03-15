# coding=utf-8
from sae.const import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB, MYSQL_HOST_S
import os
import sys

# 重载字符集
reload(sys)
sys.setdefaultencoding('utf8')

# 是否在SAE引擎上运行
IN_SAE = 'SERVER_SOFTWARE' in os.environ

# 数据库
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

# 读写分离
DATABASE_ROUTERS = ['django_sae.db.routers.MasterSlaveRouter']

# 缓存
CACHES = {
    'default': {
        'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        'TIMEOUT': 86400,
        'VERSION': 1,
    }
}

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

# 关闭多语言引擎，优化性能
USE_I18N = False

# 不开启时区，因为开启的话，保存进数据库的时间显示的将不是本地时间，而是UTC时间（需转换为本地时间）
USE_TZ = False

STATIC_URL = '/static/'