from apps.linabi.models import BICatalog

class DbRouter:

    route_app_labels = {'linabi'}
    extmodels = {BICatalog}
    extmodels_names = {'BICatalog'}

    def db_for_read(self, model, **hints):
        # if model._meta.app_label in self.route_app_labels:
        if model in self.extmodels:
            return 'extdb1'

        return None


    def db_for_write(self, model, **hints):
        # if model._meta.app_label in self.route_app_labels:
        if model in self.extmodels:
            return 'extdb1'

        return None


    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.model_name in self.extmodels_names) and (obj2._meta.model_name in self.extmodels_names):
            return False

        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'extdb1' or model_name in self.extmodels_names:
            return False

        return True
