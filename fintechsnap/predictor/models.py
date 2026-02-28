from django.db import models

class UserInput(models.Model):
    monthly_income = models.FloatField()
    total_expense = models.FloatField()
    total_emi = models.FloatField()
    savings = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Prediction(models.Model):
    user_input = models.ForeignKey(UserInput, on_delete=models.CASCADE)
    persona_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
