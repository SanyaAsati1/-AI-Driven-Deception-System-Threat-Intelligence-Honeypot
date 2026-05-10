import sqlite3

def display_logs():
    try:
        # Connect to the database your honeypot created
        conn = sqlite3.connect('honeypot_data.db')
        cursor = conn.cursor()

        # Pull all recorded attack data
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()

        if not rows:
            print("\n--- The database is empty. Start the honeypot and send some traffic! ---")
        else:
            print("\n" + "="*75)
            print(f"{'ID':<4} | {'Timestamp':<20} | {'Attacker IP':<15} | {'Message/Payload'}")
            print("="*75)
            for row in rows:
                print(f"{row[0]:<4} | {row[1]:<20} | {row[2]:<15} | {row[3]}")
            print("="*75)
            print(f"Total Logs Captured: {len(rows)}")

        conn.close()
    except sqlite3.OperationalError:
        print("\n[!] Error: 'honeypot_data.db' not found. Run your honeypot script first!")

if __name__ == "__main__":
    display_logs()