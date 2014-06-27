# coding=utf-8
from django.db import models, IntegrityError
from django.utils import timezone
from django_sae.utils.decorators import retry
import datetime

DEFAULT_RETRIES = 3  # 重试次数
DEFAULT_UPDATE_CYCLE = datetime.timedelta(weeks=1)  # 更新周期


class RepositoryBase(object):
    Model = models.Model
    PK = 'id'  # 与解析对象的ITEM_PK对应的数据库字段名
    ITEM_PK = 'id'  # 与解析对象的主键
    UPDATE_CHECK_FIELDS = []

    def distinct(self, items):
        return {self._get_item_pk(item): item for item in items}

    @classmethod
    def get_values_list(cls, *fields, **kwargs):
        return cls.Model.objects.filter(**kwargs).values_list(*fields, flat=True)

    @classmethod
    def get_not_in(cls, id_field, ids):
        ids_set = set(ids)
        kwargs = {'%s__in' % id_field: ids}
        exist_ids = cls.get_values_list(id_field, **kwargs)
        return ids_set - set(exist_ids)

    @classmethod
    def get_pk_list(cls, **kwargs):
        return cls.get_values_list(cls.PK, **kwargs)

    def get_exist_ids(self, item_ids):
        return self.get_pk_list(id__in=item_ids)

    def get_exist_objects(self, item_ids):
        return self.Model.objects.filter(id__in=item_ids)

    def get_pk_fields(self, item):
        """ 获取响应结果中的数据库主键字段
        """
        return {self.PK: self._get_item_pk(item)}

    def update_defaults_fields(self, fields, item):
        """ 更新和补充响应结果中的数据库非主键字段
        """
        pass

    def get_defaults_fields(self, item):
        """ 获取响应结果中的数据库非主键字段
        """
        fields = {}
        self.update_defaults_fields(fields, item)
        return fields

    def to_fields(self, item):
        """ 将响应结果转换为数据库字段（Dict）
        """
        fields = self.get_pk_fields(item)
        defaults = self.get_defaults_fields(item)
        if defaults:
            fields.update(defaults)
        return fields

    def build(self, item):
        return self.Model(**self.to_fields(item))

    def _pre_create(self, item):
        pass

    def create(self, item):
        self._pre_create(item)
        try:
            return self.Model.objects.create(**self.to_fields(item))
        except IntegrityError:
            return self.update_or_create(item)

    def _pre_bulk_create(self, items):
        pass

    @retry(DEFAULT_RETRIES, IntegrityError)
    def _try_bulk_create(self, items_dict):
        """如主键重复，则重新尝试"""
        all_ids = items_dict.keys()
        exist_ids = self.get_exist_ids(all_ids)
        new_ids = set(all_ids) - set(exist_ids)
        new_objects = [self.build(items_dict[k]) for k in new_ids]
        return self.Model.objects.bulk_create(new_objects)

    def bulk_create(self, items):
        """批量创建记录（忽略已存在的记录），只返回新的记录"""
        self._pre_bulk_create(items)
        items_dict = self.distinct(items)
        return self._try_bulk_create(items_dict)

    def _get_pk(self, obj):
        return getattr(obj, self.PK)

    def _get_item_pk(self, item):
        return item.get(self.ITEM_PK)

    def is_updatable(self, obj, item):
        """判断是否可更新"""
        if self.UPDATE_CHECK_FIELDS:
            for field in self.UPDATE_CHECK_FIELDS:
                if getattr(obj, field) != item.get(field):
                    return True
        return timezone.now() - obj.updated_at > DEFAULT_UPDATE_CYCLE

    def update(self, obj, item, is_check_updatable=True):
        defaults = self.get_defaults_fields(item)
        if not is_check_updatable or self.is_updatable(obj, defaults):
            for key, value in defaults.iteritems():
                setattr(obj, key, value)
            obj.save()

    def bulk_update_or_create(self, items):
        """批量创建记录，并自动更新（已存在的且超过更新周期的）记录，返回所有记录"""
        self._pre_bulk_create(items)
        items_dict = self.distinct(items)
        new_objects = self._try_bulk_create(items_dict)
        if len(items) != len(new_objects):
            new_ids = [self._get_pk(obj) for obj in new_objects]
            old_ids = set(items_dict.keys()) - set(new_ids)
            old_objects = self.get_exist_objects(old_ids)
            for obj in old_objects:
                item = items_dict[self._get_pk(obj)]
                self.update(obj, item)
            new_objects.extend(old_objects)
        return new_objects

    def get_or_create(self, item):
        self._pre_create(item)
        pk = self.get_pk_fields(item)
        defaults = self.get_defaults_fields(item)
        pk.update(defaults=defaults)
        return self.Model.objects.get_or_create(**pk)

    def update_or_create(self, item):
        self._pre_create(item)
        pk = self.get_pk_fields(item)
        try:
            obj = self.Model.objects.get(**pk)
            self.update(obj, item)
        except self.Model.DoesNotExist:
            fields = self.get_defaults_fields(item)
            fields.update(pk)
            obj = self.Model(**fields)
            obj.save()
        return obj

    def delete(self, item):
        pk = self.get_pk_fields(item)
        self.Model.objects.filter(**pk).delete()