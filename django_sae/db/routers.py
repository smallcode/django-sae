# coding=utf-8


class MasterSlaveRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads always go to slave.
        """
        return 'slave'

    def db_for_write(self, model, **hints):
        """
        Writes always go to default master.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return True