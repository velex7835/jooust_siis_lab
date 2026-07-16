from django.apps import AppConfig

class LabPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lab_portal'

    def ready(self):
        import lab_portal.signals  # Connect the resolution emails trigger signal
