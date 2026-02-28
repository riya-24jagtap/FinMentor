from django.urls import path
from .views import predict, action_plan_predict

app_name = "financeapp"   # ← REQUIRED if namespaced

urlpatterns = [
    path("", predict, name="predict"),
    path("action-plan/predict/", action_plan_predict, name="action_plan_predict"),
]
