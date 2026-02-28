from django.urls import path
from .views import analyze_finances

urlpatterns = [
    path('analyze/', analyze_finances),
]
