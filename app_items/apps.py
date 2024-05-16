from django.apps import AppConfig


class AppItemsConfig(AppConfig):
    name = 'app_items'

    # def ready(self):
    #     from jobs import updater
    #     updater.start()
