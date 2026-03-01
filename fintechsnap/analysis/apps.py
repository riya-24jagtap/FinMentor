from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'

from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

class FinanceappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financeapp'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin123"
                )
        except OperationalError:
            pass