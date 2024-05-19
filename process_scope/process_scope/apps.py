from django.apps import AppConfig

class ProcessScopeConfig(AppConfig):
    name = 'process_scope'

    def ready(self):
        import process_scope.signals
