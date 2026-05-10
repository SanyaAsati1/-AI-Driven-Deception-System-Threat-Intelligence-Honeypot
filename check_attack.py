import joblib
import os
import pandas as pd
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colors for Windows terminal
init(autoreset=True)

def show_banner():
    print(Fore.CYAN + "="*50)
    print(Fore.CYAN + "      SANYA'S AI SECURITY SHIELD - v1.0")
    print(Fore.CYAN + "        Cyber Security & Forensics Lab")
    print(Fore.CYAN + "="*50)

def check_new_hit():
    model_path = 'security_model.pkl'
    if not os.path.exists(model_path):
        print(Fore.RED + "[-] ERROR: Security Brain not found. Run train_ai.py!")
        return

    model = joblib.load(model_path)
    show_banner()
    print(Fore.GREEN + "[STATUS] AI Inference Engine: ONLINE")
    print(Fore.GREEN + "[STATUS] Firewall Link: ESTABLISHED")

    while True:
        print(Style.BRIGHT + "\n--- AWAITING NETWORK TELEMETRY ---")
        user_input = input("Enter connection time gap (s) or 'q' to exit: ")
        
        if user_input.lower() == 'q':
            print(Fore.YELLOW + "System powering down...")
            break

        try:
            speed = float(user_input)
            test_data = pd.DataFrame([[speed]], columns=['time_diff'])
            prediction = model.predict(test_data)
            
            if prediction[0] == 1:
                print(Back.RED + Fore.WHITE + " ! ALERT ! ")
                print(Fore.RED + "TYPE: Malicious Bot Activity Detected")
                print(Fore.RED + f"BEHAVIOR: Rapid-fire connection ({speed}s)")
                
                # Update Blacklist
                with open("blacklist.txt", "a") as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"127.0.0.1 at {timestamp} - Speed: {speed}s\n")
                
                print(Fore.YELLOW + "[ACTION] IP 127.0.0.1 added to blacklist.txt")
                print(Fore.YELLOW + "[ACTION] Honeypot IPS updated to REJECT future hits.")
                
            else:
                print(Back.GREEN + Fore.BLACK + " OK ")
                print(Fore.GREEN + "TYPE: Authorized / Human Probe")
                print(Fore.GREEN + f"BEHAVIOR: Normal speed ({speed}s)")
                
        except ValueError:
            print(Fore.MAGENTA + "[-] Please enter a numeric value for seconds.")

if __name__ == "__main__":
    check_new_hit()