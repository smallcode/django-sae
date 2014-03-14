# coding=utf-8


class Manager(object):
    def __init__(self):
        self.instance = None

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError(
                "%s objects need to have a primary key value before you can access their bans." % model.__name__)
        self.instance = instance
        return self

    def __getattribute__(self, item):
        if item != 'instance' and self.instance is None:
            raise ValueError(u'%s必须通过实例调用', item)
        return super(Manager, self).__getattribute__(item)