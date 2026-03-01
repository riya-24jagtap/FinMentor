# financeapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import numpy as np
from .models import FinanceRecord, ExpenseCategory, SavingsGoal
import pandas as pd
import json
import os
import joblib
from dataclasses import dataclass


PERSONA_MAP = {
    0: "Financially Moderate",
    1: "Financially Stable",
    2: "Financially Stressed"
}


# ------------------------------------------------------------------
# LANDING
# ------------------------------------------------------------------
def landing(request):
    context = {}

    if request.user.is_authenticated:
        record = FinanceRecord.objects.filter(user=request.user).first()
        context["has_data"] = bool(record)

        if record:
            context.update({
                "score": record.score,
                "monthly_income": record.income,
                "monthly_expenses": record.expenses,
                "monthly_savings": record.net_balance,
                "savings_rate": round(record.savings_rate, 1),
            })

    return render(request, "landing.html", context)

@login_required
def dashboard(request):
    record = FinanceRecord.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    if not record:
        messages.info(request, "Please fill in your financial details.")
        return redirect("input")

    user_name = request.user.first_name or request.user.username
    score = record.score or 0
    

    # ---------------- RISK LEVEL ----------------
    if score < 40:
        risk = "High Risk"
    elif score < 70:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"
    

    # ---------------- USE STORED PREDICTIONS ----------------
    svm_output = request.session.get("svm_output", "Not Available")
    crf_output = request.session.get("crf_output", "Not Available")
    hmm_output = request.session.get("hmm_output", "Not Available")

    selection_reason = request.session.get("selection_reason", "")
    # Final persona should ALWAYS match what was saved
    final_output = record.persona
    

    # ---------------- CONTEXT ----------------
    context = {
        "user_name": user_name,
        "risk": risk,
        "persona": final_output,
        "score": score,
        "spending_behaviour": record.spending_behaviour,
        "savings_behaviour": record.savings_behaviour,
        "emi_status": record.emi_status,
        "expense_ratio": round((record.expenses / record.income) * 100, 1)
            if record.income > 0 else 0,
        "emi_ratio": round((record.fixed_obligations / record.income) * 100, 1)
            if record.income > 0 else 0,
        "disposable_income": record.net_balance,
        "savings_rate": round(record.savings_rate, 1),
        "svm_output": svm_output,
        "crf_output": crf_output,
        "hmm_output": hmm_output,
        "final_output": final_output,
        "selection_reason": selection_reason,
    }

    return render(request, "dashboard.html", context)

@login_required
def loans_emi(request):
    record = FinanceRecord.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    emi_ratio = 0
    income = 0
    existing_emis = 0

    if record and record.income > 0:
        income = record.income
        existing_emis = record.fixed_obligations  # your total_emi
        emi_ratio = round((existing_emis / income) * 100, 1)

    context = {
        "income": income,
        "existing_emis": existing_emis,
        "emi_ratio": emi_ratio,
    }

    return render(request, "loans_emi.html", context)

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def action_plan(request):
    record = FinanceRecord.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    if not record:
        messages.info(request, "Please fill in your financial details.")
        return redirect("input")

    score = record.score or 0
    savings_rate = record.savings_rate or 0  # already stored as %
    emi_ratio = (record.fixed_obligations / record.income) * 100 if record.income > 0 else 0
    expense_ratio = (record.expenses / record.income) * 100 if record.income > 0 else 0

    # -------- RISK LABEL --------
    if score < 40:
        health_label = "High Risk"
    elif score < 70:
        health_label = "Moderate Risk"
    else:
        health_label = "Low Risk"

    # -------- DYNAMIC ACTION PLAN --------
    action_points = []

    if savings_rate < 20:
        action_points.append("Increase savings rate to at least 20% of income.")

    if emi_ratio > 35:
        action_points.append("Reduce EMI burden below 35% of income.")

    if expense_ratio > 60:
        action_points.append("Optimize discretionary spending to reduce expense ratio.")

    if savings_rate >= 40 and emi_ratio < 20:
        action_points.append("Consider long-term investments for wealth growth.")

    context = {
        "score": score,
        "health_label": health_label,
        "savings_rate": round(savings_rate, 1),
        "emi_to_income_pct": round(emi_ratio, 1),
        "monthly_income": record.income,
        "monthly_savings": record.net_balance,
        "monthly_expenses": record.expenses,
        "total_emi": record.fixed_obligations,
        "action_points": action_points
    }

    return render(request, "action_plan.html", context)


@csrf_exempt
@login_required
@require_POST
def action_plan_predict(request):
    try:
        data = json.loads(request.body)

        income = float(data.get("income", 0))
        expense = float(data.get("expense", 0))
        emi = float(data.get("emi", 0))
        savings = float(data.get("savings", 0))

        if income <= 0:
            return JsonResponse({"error": "Income must be greater than zero."})

        # -------- DERIVED METRICS --------
        expense_ratio = expense / income
        emi_ratio = emi / income
        savings_rate = savings / income

        # -------- SCORE FORMULA --------
        score = (
            (1 - expense_ratio) * 35 +
            (1 - emi_ratio) * 25 +
            savings_rate * 40
        )

        score = max(0, min(100, round(score, 1)))

        # -------- RISK LABEL --------
        if score < 40:
            label = "High Risk"
        elif score < 70:
            label = "Moderate Risk"
        else:
            label = "Low Risk"

        return JsonResponse({
            "new_score": score,
            "label": label,
            "expense_ratio": round(expense_ratio * 100, 1),
            "emi_ratio": round(emi_ratio * 100, 1),
            "savings_rate": round(savings_rate * 100, 1)
        })

    except Exception:
        return JsonResponse({"error": "Invalid input data."})

@login_required
def edit_expenses(request):
    return render(request, "edit_expenses.html")

@login_required
def add_goal(request):
    return render(request, "add_goal.html")
@login_required
def edit_goal(request, goal_id):
    return render(request, "edit_goal.html", {"goal_id": goal_id})

@login_required
def delete_goal(request, goal_id):
    # safe stub – actual delete logic can be added later
    return redirect("savings")


@login_required
def spending_insights(request):
    record = FinanceRecord.objects.filter(user=request.user).order_by("-created_at").first()

    if not record:
        messages.info(request, "Please fill in your financial details to view spending insights.")
        return redirect("input")
    expense_income_ratio = round(
        (record.expenses / record.income) * 100, 1
    ) if record.income > 0 else 0

    categories = ExpenseCategory.objects.filter(user=request.user)
    total_expenses = sum(c.amount for c in categories) if categories else 0

    cat_data = []
    for c in categories:
        percent = round((c.amount / total_expenses) * 100, 1) if total_expenses > 0 else 0
        cat_data.append({
            "name": c.name,
            "amount": c.amount,
            "percent": percent,
            "type": c.type,
        })

    top_category_name = None
    top_category_pct = None
    if cat_data:
        top = max(cat_data, key=lambda x: x["amount"])
        top_category_name = top["name"]
        top_category_pct = top["percent"]

    essentials_total = sum(c["amount"] for c in cat_data if c["type"] == "Essential")
    discretionary_total = sum(c["amount"] for c in cat_data if c["type"] == "Discretionary")

    essentials_pct = round((essentials_total / total_expenses) * 100, 1) if total_expenses > 0 else 0
    discretionary_pct = round((discretionary_total / total_expenses) * 100, 1) if total_expenses > 0 else 0
    
    chart_labels = [c["name"] for c in cat_data]
    chart_values = [c["amount"] for c in cat_data]

    
    context = {
        "monthly_expenses": record.expenses,
        "categories": cat_data,
        "top_category_name": top_category_name,
        "top_category_pct": top_category_pct,
        "essentials_pct": essentials_pct,
        "discretionary_pct": discretionary_pct,
        "persona": record.persona,                
        "spending_behaviour": record.spending_behaviour, 
        "expense_income_ratio": expense_income_ratio, 
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "monthly_income": record.income,
    }

    return render(request, "spending.html", context)


# ------------------------------------------------------------------
# SAVINGS
# ------------------------------------------------------------------
@login_required
def savings_goals(request):
    record = FinanceRecord.objects.filter(user=request.user).order_by("-created_at").first()

    if not record:
        messages.info(request, "Please fill in your financial details.")
        return redirect("input")

    savings_rate = record.savings_rate or 0

    if savings_rate >= 30:
        savings_health_label = "Strong"
    elif savings_rate >= 15:
        savings_health_label = "Moderate"
    else:
        savings_health_label = "Needs Improvement"

    coverage_months = 0
    if record.expenses > 0:
        coverage_months = round(record.net_balance / record.expenses, 1)

    goals = SavingsGoal.objects.filter(user=request.user)

    context = {
        "monthly_savings": record.net_balance,
        "savings_rate": round(savings_rate, 1),
        "coverage_months": coverage_months,
        "savings_health_label": savings_health_label,
        "goals": goals,
        "persona": record.persona,
    }

    return render(request, "savings.html", context)

@login_required
def input_page(request):
    record = FinanceRecord.objects.filter(user=request.user).order_by("-created_at").first()
    categories = ExpenseCategory.objects.filter(user=request.user)

    category_dict = {}

    for cat in categories:
        key = cat.name.replace(" ", "_")
        category_dict[key] = cat.amount

    return render(request, "input.html", {
        "record": record,
        "category": category_dict
    })

@login_required
def compute_health(request):
    if request.method != "POST":
        return redirect("input")

    # ---------------- USER INPUT ----------------
    income = float(request.POST.get("income", 0) or 0)
    fixed = float(request.POST.get("fixed", 0) or 0)

    rent = float(request.POST.get("rent", 0) or 0)
    groceries = float(request.POST.get("groceries", 0) or 0)
    transport = float(request.POST.get("transport", 0) or 0)
    utilities = float(request.POST.get("utilities", 0) or 0)
    dining_out = float(request.POST.get("dining_out", 0) or 0)
    shopping = float(request.POST.get("shopping", 0) or 0)
    entertainment = float(request.POST.get("entertainment", 0) or 0)
    healthcare = float(request.POST.get("healthcare", 0) or 0)
    education = float(request.POST.get("education", 0) or 0)

    if income <= 0:
        messages.error(request, "Income must be greater than zero.")
        return redirect("input")

    # ---------------- CALCULATE TOTAL EXPENSES ----------------
    expenses = (
        rent + groceries + transport + utilities +
        dining_out + shopping + entertainment +
        healthcare + education
    )

    # ---------------- DERIVED METRICS ----------------
    net_balance = income - expenses - fixed
    savings_rate = net_balance / income if income > 0 else 0
    emi_ratio = fixed / income if income > 0 else 0
    expense_ratio = expenses / income if income > 0 else 0

    # ---------------- NUMERIC ENCODING (FOR ML) ----------------
    savings_numeric = 0 if savings_rate >= 0.2 else 1
    spending_numeric = 0 if expense_ratio < 0.6 else 1
    emi_numeric = 1 if emi_ratio < 0.4 else 0

    # ---------------- LABELS (FOR DASHBOARD DISPLAY) ----------------
    savings_label = "Good Saver" if savings_numeric == 0 else "Low Saver"
    spending_label = "Moderate Spender" if spending_numeric == 0 else "High Spender"
    emi_label = "Normal EMI" if emi_numeric == 1 else "High EMI Burden"

    # ---------------- BUILD FEATURE VECTOR FOR ML ----------------
    X_raw = [[
        income,
        expenses,
        fixed,
        emi_ratio,
        expense_ratio,
        savings_numeric,
        emi_numeric,
        spending_numeric,
        net_balance,
        savings_rate
    ]]
    


    from pathlib import Path

    MODEL_DIR = Path(__file__).resolve().parent.parent / "ml_models"

    svm_model = joblib.load(MODEL_DIR / "svm_model.pkl")
    hmm_model = joblib.load(MODEL_DIR / "hmm_model.pkl")
    crf_model = joblib.load(MODEL_DIR / "crf_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    # Scale input
    X_scaled = scaler.transform(X_raw)

    # SVM prediction
    svm_pred = int(svm_model.predict(X_scaled)[0])

    # HMM prediction
    hmm_pred = int(hmm_model.predict(X_scaled)[0])

    # CRF prediction
    X_crf = [[{
        "monthly_income": income,
        "total_expense": expenses,
        "total_emi": fixed,
        "emi_ratio": emi_ratio,
        "expense_ratio": expense_ratio,
        "savings_behaviour": savings_numeric,
        "emi_status": emi_numeric,
        "spending_behaviour": spending_numeric,
        "net_balance": net_balance,
        "savings_rate": savings_rate
    }]]

    crf_pred = int(crf_model.predict(X_crf)[0][0])

    # ---------------- HYBRID ENSEMBLE VOTING ----------------
    from collections import Counter

    predictions = [svm_pred, crf_pred, hmm_pred]
    counter = Counter(predictions)

    most_common_label, count = counter.most_common(1)[0]

    if count >= 2:
        agreeing_models = []
        if svm_pred == most_common_label:
            agreeing_models.append("SVM")
        if crf_pred == most_common_label:
            agreeing_models.append("CRF")
        if hmm_pred == most_common_label:
            agreeing_models.append("HMM")

        final_pred = most_common_label
        selection_reason = (
            "Selected based on majority agreement between "
            + " and ".join(agreeing_models) + "."
        )
    else:
        # override logic
        if savings_rate >= 0.4 and emi_ratio <= 0.1 and expense_ratio <= 0.5:
            final_pred = 1
            selection_reason = "Selected based on financial consistency override."
        elif savings_rate <= 0.1 or emi_ratio >= 0.5:
            final_pred = 2
            selection_reason = "Selected based on financial stress override."
        else:
            final_pred = svm_pred
            selection_reason = "Selected based on primary model (SVM)."
    # ---------------- MAP FINAL PERSONA ----------------
    persona = PERSONA_MAP.get(final_pred, "Unknown")
    # 🔥 MOVE THIS OUTSIDE
    request.session["selection_reason"] = selection_reason
    # ---------------- FINANCIAL HEALTH SCORE (0–100) ----------------
    score = (
        (1 - expense_ratio) * 35 +
        (1 - emi_ratio) * 25 +
        savings_rate * 40
    )

    score = max(0, min(100, round(score, 1)))

    # ---------------- SAVE TO DATABASE ----------------
    record, _ = FinanceRecord.objects.get_or_create(user=request.user)

    record.income = income
    record.expenses = expenses
    record.fixed_obligations = fixed
    record.net_balance = net_balance
    record.savings_rate = savings_rate * 100  # store as percentage
    record.score = score
    record.persona = persona
    record.savings_behaviour = savings_label
    record.spending_behaviour = spending_label
    record.emi_status = emi_label
    record.save()
    print("SVM:", svm_pred)
    print("HMM:", hmm_pred)
    print("CRF:", crf_pred)
    print("FINAL:", final_pred)

    # ---------------- SAVE CATEGORY BREAKDOWN ----------------
    ExpenseCategory.objects.filter(user=request.user).delete()

    ExpenseCategory.objects.create(user=request.user, name="Rent", amount=rent, type="Essential")
    ExpenseCategory.objects.create(user=request.user, name="Groceries", amount=groceries, type="Essential")
    ExpenseCategory.objects.create(user=request.user, name="Transport", amount=transport, type="Essential")
    ExpenseCategory.objects.create(user=request.user, name="Utilities", amount=utilities, type="Essential")
    ExpenseCategory.objects.create(user=request.user, name="Healthcare", amount=healthcare, type="Essential")
    ExpenseCategory.objects.create(user=request.user, name="Education", amount=education, type="Essential")

    ExpenseCategory.objects.create(user=request.user, name="Dining Out", amount=dining_out, type="Discretionary")
    ExpenseCategory.objects.create(user=request.user, name="Shopping", amount=shopping, type="Discretionary")
    ExpenseCategory.objects.create(user=request.user, name="Entertainment", amount=entertainment, type="Discretionary")

    messages.success(request, "Your financial profile has been updated successfully.")
    request.session["svm_output"] = PERSONA_MAP.get(svm_pred, "Unknown")
    request.session["crf_output"] = PERSONA_MAP.get(crf_pred, "Unknown")
    request.session["hmm_output"] = PERSONA_MAP.get(hmm_pred, "Unknown")
    request.session["final_output"] = persona
    return redirect("dashboard")


# ------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------
def about(request):
    return render(request, "about.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
