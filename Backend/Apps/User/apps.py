from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'Apps.User'

    def ready(self):
        import Apps.User.signals

