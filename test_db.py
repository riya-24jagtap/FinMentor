import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="finmentor_db"
)

print("MySQL connection successful")
conn.close()
