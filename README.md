#django-sae

[![PyPI version](https://badge.fury.io/py/django-sae.png)](http://badge.fury.io/py/django-sae)

用于新浪云平台SAE  

### 扩展命令
* compress_site_packages：压缩 site_packages
* sae_migrate：切换到SAE数据库，并进行migrate操作(注1）
* sae_schemamigration：切换到SAE数据库，并进行schemamigration操作
* sae_syncdb：切换到SAE数据库，并进行syncdb操作

### 缓存
使用 SAE Memcache 服务，在settings中进行如下设置:
```python
    CACHES={
        'default': {
            'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        }
    }
```
