import pandas as pd
import mysql.connector

# Load dataset
df = pd.read_excel(r"D:\riya\Finmentor_Data_TRANSFORMED_FINAL.xlsx")

print("Columns:", df.columns.tolist())

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="finmentor_db"
)

cursor = conn.cursor()

# Optional: avoid duplicate inserts
cursor.execute("TRUNCATE TABLE financial_dataset")

# Insert mapped data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO financial_dataset
        (income, expense, savings, emi,
         expense_ratio, savings_rate, emi_ratio, persona)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["monthly_income"],     # income
        row["total_expense"],      # expense
        row["current_savings"],    # savings
        row["total_emi"],          # emi
        row["expense_ratio"],
        row["savings_rate"],
        row["emi_ratio"],
        row["persona"]
    ))

conn.commit()
print("Dataset inserted successfully")
