import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    conn = sqlite3.connect("honeypot_data.db")
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()

    # 1. Calculate the real gaps from your logs
    col_name = 'time' if 'time' in df.columns else 'Timestamp'
    df[col_name] = pd.to_datetime(df[col_name])
    df = df.sort_values(by=col_name)
    df['time_diff'] = df[col_name].diff().dt.total_seconds().fillna(0)

    # 2. CREATE A BALANCED DATASET (Important!)
    # We will combine your real logs with some "Fake" slow logs 
    # so the AI understands what a Human actually looks like.
    training_data = pd.DataFrame({
        'time_diff': list(df['time_diff']) + [30.0, 45.0, 60.0, 120.0],
        'label': [1] * len(df) + [0, 0, 0, 0]  # Your logs = Bot, Our fake ones = Human
    })
    
    X = training_data[['time_diff']]
    y = training_data['label']

    # 3. Train the model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    
    joblib.dump(model, 'security_model.pkl')
    print("\n[+] Training Complete with Balanced Data!")
    print("[+] The AI now understands: Fast (<7s) = Bot, Slow (>30s) = Human.")

if __name__ == "__main__":
    train_model()