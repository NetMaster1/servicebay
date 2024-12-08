from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    name = 'app_users'

def ready (self):
    from jobs import updater
    updater.start()