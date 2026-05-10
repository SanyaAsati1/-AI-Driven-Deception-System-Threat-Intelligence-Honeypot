import socket
import sqlite3
import os
from datetime import datetime
from cryptography.fernet import Fernet

# --- 1. ENCRYPTION SETUP ---
def load_key():
    """Loads the secret key from the current directory."""
    if not os.path.exists("secret.key"):
        print("❌ ERROR: secret.key not found! Run your key_generator.py first.")
        exit()
    return open("secret.key", "rb").read()

# Initialize the Cipher Suite
cipher_suite = Fernet(load_key())

def start_honeypot():
    # --- 2. FORENSIC DATABASE SETUP ---
    conn_db = sqlite3.connect("honeypot_data.db")
    curr = conn_db.cursor()
    
    # We use IF NOT EXISTS so we don't delete your data every time you restart
    curr.execute("""CREATE TABLE IF NOT EXISTS logs (
                    source_ip TEXT, 
                    dest_port INTEGER, 
                    date TEXT, 
                    day TEXT, 
                    time TEXT)""")
    conn_db.commit()

    # --- 3. NETWORK SOCKET SETUP ---
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        port = 5050
        s.bind(('0.0.0.0', port)) 
        s.listen(5)
    except Exception as e:
        print(f"❌ Bind failed: {e}")
        return
    
    print("🛡️  SANYA'S AI SECURITY SHIELD - ACTIVE")
    print(f"📍 MONITORING PORT: {port}")
    print("🔒 AES-256 ENCRYPTION: ENABLED")

    while True:
        try:
            client_conn, addr = s.accept()
            attacker_ip = addr[0]

            # --- 4. CAPTURE FORENSIC METADATA ---
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            day_str = now.strftime("%A") 
            time_str = now.strftime("%H:%M:%S")

            # --- 5. THE AES ENCRYPTION STEP ---
            # We encrypt the IP address so it's unreadable in the raw database file
            encrypted_ip = cipher_suite.encrypt(attacker_ip.encode()).decode()

            # --- 6. THE DECEPTION LAYER ---
            banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n"
            client_conn.send(banner.encode())
            
            print(f"⚠️  DECEPTION SUCCESSFUL: {attacker_ip} logged (Encrypted in DB)")
            
            # --- 7. LOG INTO ENCRYPTED SQL PIPELINE ---
            curr.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", 
                         (encrypted_ip, port, date_str, day_str, time_str))
            conn_db.commit()
            
            client_conn.close()
        except Exception as e:
            print(f"Log Error: {e}")
            pass

if __name__ == "__main__":
    start_honeypot()