#django-sae

[![PyPI version](https://badge.fury.io/py/django-sae.png)](http://badge.fury.io/py/django-sae)

用于新浪云平台SAE  

### 扩展命令
* compress_site_packages：压缩 site_packages
* sae_migrate：切换到SAE数据库，并进行migrate操作
* sae_schemamigration：切换到SAE数据库，并进行schemamigration操作
* sae_syncdb：切换到SAE数据库，并进行syncdb操作

使用sae_migrate、sae_schemamigration、sae_syncdb等数据库相关的扩展命令时，请在settings中进行如下设置:
```python
    MYSQL_DB=u'SAE数据库名称'
    MYSQL_USER=u'SAE数据库用户名称'
    MYSQL_PASS=u'SAE数据库用户密码'
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