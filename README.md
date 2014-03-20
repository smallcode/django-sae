#django-sae

[![PyPI version](https://badge.fury.io/py/django-sae.png)](http://badge.fury.io/py/django-sae)

用于新浪云平台SAE  

### 扩展命令
* compress_site_packages：压缩 site_packages
* upgrade_requirements：更新requirements.txt中所有依赖的库
* sae_migrate：切换到SAE数据库，并进行migrate操作
* sae_syncdb：切换到SAE数据库，并进行syncdb+migrate操作

使用sae_migrate、sae_syncdb等与数据库相关的扩展命令时，请手工获取SAE数据库的相关常数，如MYSQL_DB、MYSQL_USER、MYSQL_PASS等，并在settings中对DATABASES进行修改。

### 数据库
如需数据库读写操作分离，请在settings中进行如下设置:
```python
    from sae.const import MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
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
    DATABASE_ROUTERS = ['django_sae.db.routers.MasterSlaveRouter']
```

### 缓存
使用 SAE Memcache 服务时，请在settings中进行如下设置:
```python
    CACHES={
        'default': {
            'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        }
    }
```