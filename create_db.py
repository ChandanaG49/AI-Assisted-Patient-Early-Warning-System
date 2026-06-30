
import sqlite3

conn = sqlite3.connect("database.db")

cur = conn.cursor()

# Users Table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT,
password TEXT
)
""")

# Patients Table
cur.execute("""
CREATE TABLE IF NOT EXISTS patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_name TEXT,
age INTEGER,
sex TEXT,
bp INTEGER,
chol INTEGER,
maxhr INTEGER,
oldpeak REAL,
result TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS appointments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_name TEXT,
doctor TEXT,
appointment_date TEXT,
appointment_time TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")

