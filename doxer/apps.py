from django.apps import AppConfig


class DoxerConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'doxer'
    
    # def ready(self):
    #     from jobs import updater
    #     updater.start()