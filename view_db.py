import sqlite3

db = sqlite3.connect("ransomware_database.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM victims")
for row in cursor.fetchall():
    print(row)
db.close()


