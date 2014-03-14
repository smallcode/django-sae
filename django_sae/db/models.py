# coding=utf-8
from django.db import models
from django.utils import timezone


class AutoIdEntity(models.Model):
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        """
        __unicode__和__str__用于显示（给人看的）,__str__返回字节（bytes），__unicode__返回字符（characters）
        __repr__ 用于判断（给解释器看的）
        """
        return unicode(self.id)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super(AutoIdEntity, self).save(*args, **kwargs)


class LongIdEntity(AutoIdEntity):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        abstract = True