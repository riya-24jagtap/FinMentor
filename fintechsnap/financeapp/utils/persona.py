# finmentor/utils/persona.py

from dataclasses import dataclass

@dataclass
class PersonaInfo:
    key: str
    title: str
    long_message: str
    short_badge: str
    tagline: str

def determine_spender_persona(
    monthly_income: float,
    total_expenses: float,
    discretionary_expenses: float,
    total_emi: float = 0.0,
) -> PersonaInfo:
    """
    Rule-based persona classification.
    Assumes:
      - monthly_income, total_expenses, discretionary_expenses, total_emi are >= 0
      - discretionary_expenses <= total_expenses
    """

    # Safety checks
    if monthly_income <= 0 or total_expenses <= 0:
        # Not enough data to classify properly → treat as Beginner
        return PersonaInfo(
            key="beginner",
            title="Beginner",
            long_message=(
                "You are in the early stage of building financial structure and spending awareness. "
                "With better tracking habits and clearer allocation, you can steadily develop stronger "
                "control over your monthly finances. You’re on the right path—continued attention "
                "will accelerate progress."
            ),
            short_badge="Early in financial tracking — building good habits will strengthen control.",
            tagline="Awareness is forming — keep building consistency.",
        )

    discretionary_ratio = discretionary_expenses / total_expenses  # 0–1
    savings = max(monthly_income - total_expenses - total_emi, 0)
    savings_rate = savings / monthly_income  # 0–1
    emi_ratio = total_emi / monthly_income if monthly_income > 0 else 0

    # --- RULES ---

    # 1) Debt-Risk: high EMI burden or very thin savings with EMI
    if emi_ratio >= 0.4 or (emi_ratio >= 0.3 and savings_rate < 0.1):
        return PersonaInfo(
            key="debt_risk",
            title="Debt-Risk",
            long_message=(
                "Your current expenses and obligations may be placing pressure on your financial capacity. "
                "Prioritising essential spending, limiting non-essential outflow, and avoiding new commitments "
                "will help reduce financial strain. With focused steps, you can move toward a more secure position."
            ),
            short_badge="Financial load is high — reduce commitments to regain stability.",
            tagline="Stabilise expenses to protect financial health.",
        )

    # 2) Overspender: high discretionary ratio + low savings
    if discretionary_ratio >= 0.30 and savings_rate < 0.15:
        return PersonaInfo(
            key="overspender",
            title="Overspender",
            long_message=(
                "Your discretionary spending is higher than recommended compared to your income and essentials. "
                "With a few adjustments, you can gradually redirect more towards savings and strengthen financial "
                "stability. Small, consistent changes will create a noticeable improvement over time."
            ),
            short_badge="Higher discretionary spending — adjust gradually to improve balance.",
            tagline="Shift spending to support savings growth.",
        )

    # 3) Beginner: very low savings rate, but not strongly overspending or debt-heavy
    if savings_rate < 0.05:
        return PersonaInfo(
            key="beginner",
            title="Beginner",
            long_message=(
                "You are in the early stage of building financial structure and spending awareness. "
                "With better tracking habits and clearer allocation, you can steadily develop stronger "
                "control over your monthly finances. You’re on the right path—continued attention "
                "will accelerate progress."
            ),
            short_badge="Early in financial tracking — building good habits will strengthen control.",
            tagline="Awareness is forming — keep building consistency.",
        )

    # 4) Balanced: default if none of the above triggers
    return PersonaInfo(
        key="balanced",
        title="Balanced",
        long_message=(
            "Your spending behaviour shows a healthy distribution between essential needs and discretionary choices. "
            "With a slight increase in savings and mindful monitoring, you can further enhance long-term "
            "financial resilience. Maintain this momentum to keep improving."
        ),
        short_badge="Healthy spending pattern — maintain discipline and grow savings.",
        tagline="Strong foundation — continue refining habits.",
    )
