from django.db import models
from django.contrib.auth.models import User

class FinanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    income = models.FloatField()
    expenses = models.FloatField()
    net_balance = models.FloatField()
    savings_rate = models.FloatField()
    fixed_obligations = models.FloatField(default=0)
    score = models.IntegerField()
    persona = models.CharField(max_length=50, blank=True)
    spending_behaviour = models.CharField(max_length=50, blank=True)
    savings_behaviour  = models.CharField(max_length=50, blank=True)
    emi_status         = models.CharField(max_length=50, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score} ({self.created_at.date()})"

class ExpenseCategory(models.Model):
    CATEGORY_TYPES = [
        ("Essential", "Essential"),
        ("Discretionary", "Discretionary"),
        ("Mixed", "Mixed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
    
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.FloatField()
    saved_amount = models.FloatField(default=0)  # NEW ✅
    allocation_percent = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percent(self):
        if self.target_amount > 0:
            return min(int((self.saved_amount / self.target_amount) * 100), 100)
        return 0

    def estimated_months_to_reach(self, monthly_savings):
        allocated = (self.allocation_percent / 100) * monthly_savings
        if allocated > 0:
            remaining = max(self.target_amount - self.saved_amount, 0)
            return round(remaining / allocated, 1)
        return None

class EmiProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_income = models.FloatField()
    existing_emi = models.FloatField()
    other_obligations = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
