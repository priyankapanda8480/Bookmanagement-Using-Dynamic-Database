from threading import local
from django.conf import settings

_thread_locals = local()

def get_current_request():
        return getattr(_thread_locals, 'request', None)

class DynamicDbRouter:
    def db_for_read(self, model, **hints):
        request = get_current_request()
        if request and hasattr(request, 'use_dynamic_db') and request.use_dynamic_db:
            return 'dynamic_db'
        return 'default'
    def db_for_write(self, model, **hints):
        request = get_current_request()
        if request and hasattr(request, 'use_dynamic_db') and request.use_dynamic_db:
            return 'dynamic_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = hints.get('database') or self.db_for_read(obj1)
        db_obj2 = hints.get('database') or self.db_for_read(obj2)
        return db_obj1 == db_obj2


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'
