import os
import joblib
from django.conf import settings
from django.shortcuts import render
from .models import UserInput, Prediction
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

PERSONA_MODEL_PATH = os.path.join(
    settings.BASE_DIR, "ml_models", "svm_model.pkl"
)

SCALER_PATH = os.path.join(
    settings.BASE_DIR, "ml_models", "scaler.pkl"
)

persona_model = joblib.load(PERSONA_MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

PERSONA_MAP = {
    0: "Financially Moderate",
    1: "Financially Stable",
    2: "Financially Stressed"
}

# SPENDING_MAP = {
#     0: "High Spender",
#     1: "Moderate Spender",
# }

# SAVINGS_MAP = {
#     0: "Low Saver",
#     1: "Good Saver",
# }

# EMI_MAP = {
#     0: "Normal EMI",
#     1: "High EMI Burden",
# }



def predict(request):
    if request.method == "POST":
        # 1️⃣ Read inputs
        monthly_income = float(request.POST["monthly_income"])
        total_expense = float(request.POST["total_expense"])
        total_emi = float(request.POST["total_emi"])
        savings = float(request.POST["savings"])

        # 2️⃣ Basic validation
        if monthly_income <= 0:
            return render(request, "form.html", {
                "error": "Monthly income must be greater than zero"
            })

        # 3️⃣ Save user input
        user = UserInput.objects.create(
            monthly_income=monthly_income,
            total_expense=total_expense,
            total_emi=total_emi,
            savings=savings
        )

        # Feature Engineering (MUST MATCH TRAINING)

        emi_ratio = total_emi / monthly_income
        expense_ratio = total_expense / monthly_income
        net_balance = monthly_income - total_expense - total_emi
        savings_rate = savings / monthly_income

        # Behaviour encoding (match dataset logic exactly)
        savings_behaviour = 1 if savings_rate >= 0.2 else 0
        emi_status = 1 if emi_ratio >= 0.4 else 0
        spending_behaviour = 1 if expense_ratio < 0.6 else 0

        # Build feature vector in SAME ORDER as training
        X_raw = [[
            monthly_income,
            total_expense,
            total_emi,
            emi_ratio,
            expense_ratio,
            savings_behaviour,
            emi_status,
            spending_behaviour,
            net_balance,
            savings_rate
        ]]


        X = scaler.transform(X_raw)

        # 5Predict class
        persona_label = int(persona_model.predict(X)[0])

        print("Predicted label:", persona_label)

        # Decode persona
        persona = PERSONA_MAP.get(persona_label, "Unknown")

        # Save prediction
        Prediction.objects.create(
            user_input=user,
            persona_score=persona_label
        )

        # Return readable result
        return render(
            request,
            "result.html",
            {"persona": persona}
        )

    return render(request, "form.html")


