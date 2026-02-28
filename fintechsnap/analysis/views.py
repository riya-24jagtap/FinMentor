from django.http import JsonResponse
import pandas as pd

PERSONA_MAP = {
    0: "Financially Moderate",
    1: "Financially Stable",
    2: "Financially Stressed"
}

def analyze_finances(request):
    income = float(request.GET.get("monthly_income", 0) or 0)
    total_emi = float(request.GET.get("total_emi", 0) or 0)
    net_balance = float(request.GET.get("net_balance", 0) or 0)

    df = pd.read_excel(r"D:\riya\Finmentor_Data_TRANSFORMED_FINAL.xlsx")

    df["distance"] = (
        (df["monthly_income"] - income).abs() +
        (df["total_emi"] - total_emi).abs() +
        (df["net_balance"] - net_balance).abs()
    )

    row = df.sort_values("distance").iloc[0]

    # ✅ decode persona
    persona_code = int(row["persona"])
    persona_label = PERSONA_MAP.get(persona_code, "Unknown")

    # ✅ spending behaviour already text
    spending_label = str(row["spending_behaviour"])

    return JsonResponse({
        "spending_behaviour": spending_label,
        "persona": persona_label
    })
