from django.apps import AppConfig


class EntertainmentConfig(AppConfig):
    name = 'entertainment'

    def ready(self):
        import entertainment.signals.handlers
