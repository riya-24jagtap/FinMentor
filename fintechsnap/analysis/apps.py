from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'

from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

class FinanceappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financeapp'

