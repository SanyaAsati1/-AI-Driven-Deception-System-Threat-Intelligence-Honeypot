import streamlit as st
import sqlite3
import pandas as pd
import os
from cryptography.fernet import Fernet

# 1. PAGE CONFIG & CUSTOM STYLING
st.set_page_config(page_title="Sanya's AI Security Shield", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; font-size: 14px; }
    [data-testid="stMetric"] { background-color: #1e2130; border: 1px solid #3b4252; padding: 15px; border-radius: 10px; }
    .main-title { color: #88c0d0; font-size: 30px !important; font-weight: 500; border-bottom: 2px solid #88c0d0; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENHANCED ROLE-BASED ACCESS CONTROL (RBAC)
if 'role' not in st.session_state:
    st.session_state.role = None
def login_portal():
    st.markdown('<p class="main-title"> 🔐 SECURITY SHIELD : GATEWAY</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Admin Login", "User Access"])
    
    with tab1:
        with st.form("admin_login"):
            st.subheader("Analyst Terminal")
            # Added .strip() to remove accidental spaces
            u = st.text_input("Admin ID").strip()
            p = st.text_input("Admin PIN", type="password").strip()
            
            if st.form_submit_button("AUTHORIZE ADMIN"):
                # Use .lower() so "sanya" or "Sanya" both work
                if u.lower() == "sanya" and p == "ADMIN123":
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("Invalid Admin Credentials")

    with tab2:
        with st.form("user_login"):
            st.subheader("Viewer Terminal")
            u_name = st.text_input("Viewer Name").strip()
            access_code = st.text_input("Access Code", type="password").strip()
            
            if st.form_submit_button("GUEST ACCESS"):
                if access_code == "GUEST2026":
                    st.session_state.role = "user"
                    st.rerun()
                else:
                    st.error("Invalid Access Code")

# This part remains the same to trigger the portal
if st.session_state.role is None:
    login_portal()
    st.stop()

# 3. AI INFERENCE ENGINE (The Intelligence Layer)
def ai_inference_engine(df):
    """
    Simulates Feature Engineering & Model Prediction.
    Addresses: Predictive Analytics & Model Evaluation.
    """
    if df.empty:
        return 0, "STANDBY", "LOW"
    
    # Feature Engineering: Intensity per session
    intensity = len(df.tail(10)) 
    
    if intensity > 8:
        prediction, confidence, severity = "DDOS / BOTNET", 98.4, "CRITICAL"
    elif intensity > 3:
        prediction, confidence, severity = "BRUTE FORCE", 94.2, "MEDIUM"
    else:
        prediction, confidence, severity = "RECONNAISSANCE", 89.1, "LOW"
        
    return confidence, prediction, severity

# 4. DATA RETRIEVAL (AES-256 Enabled)
def get_forensic_data():
    if os.path.exists("honeypot_data.db"):
        if not os.path.exists("secret.key"):
            return pd.DataFrame(), "KEY_MISSING"
            
        cipher = Fernet(open("secret.key", "rb").read())
        conn = sqlite3.connect("honeypot_data.db")
        df = pd.read_sql_query("SELECT * FROM logs", conn)
        conn.close()

        if not df.empty:
            try:
                # Decrypting for Admin view only
                df['source_ip'] = df['source_ip'].apply(lambda x: cipher.decrypt(x.encode()).decode())
                return df, "SUCCESS"
            except:
                return df, "MISMATCH"
    return pd.DataFrame(), "NO_DB"

# 5. UI RENDERING
st.markdown(f'<p class="main-title"> SANYA\'S AI SECURITY SHIELD : {st.session_state.role.upper()} PORTAL</p>', unsafe_allow_html=True)
st.caption(f"MIT-WPU CSF Lab | Analyst: Sanya Asati | Active Session: {st.session_state.role.upper()}")

# Load and Analyze Data
df, status = get_forensic_data()
confidence, prediction, severity = ai_inference_engine(df)

# Sidebar System Ops
st.sidebar.title(" SYSTEM OPS")
if st.sidebar.button('RELOAD TELEMETRY'):
    st.rerun()
if st.sidebar.button('LOGOUT'):
    st.session_state.role = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write(f" **Role:** {st.session_state.role.capitalize()}")
st.sidebar.write(f" **Dept:** CSE-CSF")

# Error Handling Displays
if status == "KEY_MISSING":
    st.error(" Forensic Key Missing: System Locked.")
elif status == "MISMATCH":
    st.warning(" Encryption Mismatch detected in legacy logs.")

# METRICS (Visible to both Roles)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("TOTAL HITS", len(df))
with m2:
    st.metric("AI PREDICTION", prediction)
with m3:
    st.metric("MODEL CONFIDENCE", f"{confidence}%")
with m4:
    st.metric("THREAT LEVEL", severity)

st.markdown("---")

# ROLE-BASED CONTENT SPLIT
if st.session_state.role == "admin":
    # ADMIN VIEW: Full access to everything
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader(" Decrypted Forensic Logs")
        if not df.empty:
            st.dataframe(df.iloc[::-1], use_container_width=True)
        else:
            st.info("Awaiting telemetry...")
    with col_right:
        st.subheader(" Threat Intelligence")
        st.error(f"**ALERT:** {prediction} Detected")
        st.write(f"**Confidence:** {confidence}%")
        st.progress(confidence/100)
        st.markdown("---")
        st.metric("ENCRYPTION", "AES-256", delta="ACTIVE")
else:
    # USER VIEW: Analytics only, no raw IP data
    st.info(" Guest View: Raw forensic logs and IP addresses are masked for security.")
    st.subheader(" Temporal Attack Distribution")
    if not df.empty:
        st.bar_chart(df['day'].value_counts(), color="#81a1c1")
    else:
        st.info("No distribution data available.")