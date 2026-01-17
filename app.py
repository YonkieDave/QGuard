import streamlit as st
import cv2
import numpy as np
import pickle

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="QGuard", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div.stButton > button { width: 100%; background-color: #ff4b4b; color: white; }
    div[data-testid="stExpander"] { background-color: #262730; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD AI MODEL ---
try:
    with open("phishing_model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ Error: 'phishing_model.pkl' not found.")
    st.stop()

# --- HELPER FUNCTIONS ---
def get_features(url):
    url = str(url)
    return [
        len(url), url.count('.'), url.count('@'), 
        url.count('-'), 1 if "https" in url else 0, 
        sum(c.isdigit() for c in url)
    ]

def check_whitelist(url):
    safe_keywords = ["upi://", "paytm", "phonepe", "gpay", "bhim", "google.com", "amazon"]
    for keyword in safe_keywords:
        if keyword.lower() in url.lower():
            return True
    return False

# --- IMPROVED HYBRID ANALYSIS LOGIC ---
def analyze_url(url):
    if not url:
        return None, None, None
    
    url_lower = url.lower()

    # STEP 1: VERIFIED PAYMENT (Whitelist)
    payment_keywords = ["upi://", "paytm", "phonepe", "gpay", "bhim"]
    for keyword in payment_keywords:
        if keyword in url_lower:
            return (0, 165, 255), f"✅ **VERIFIED PAYMENT**\n\nLINK: `{url}`", "warning"

    # STEP 2: SAFE WEBSITES (Whitelist)
    safe_domains = ["google.com", "amazon.com", "microsoft.com", "youtube.com", "wikipedia.org"]
    for domain in safe_domains:
        if domain in url_lower:
             return (0, 255, 0), f"✅ **SAFE WEBSITE**\n\nLINK: `{url}`", "success"

    # STEP 3: INSTANT DANGER TRAP (Blacklist) -> THE NEW FIX
    # If the URL contains these obvious phishing phrases, mark it DANGER immediately.
    danger_patterns = [
        "verify-account", "update-password", "secure-login", 
        "confirm-id", "paypal-manager", "bank-update", "account-suspended"
    ]
    for pattern in danger_patterns:
        if pattern in url_lower:
             return (0, 0, 255), f"🚨 **DANGER: PHISHING PATTERN DETECTED!**\n\nLINK: `{url}`", "error"

    # STEP 4: AI BRAIN (For everything else)
    features = np.array([get_features(url)])
    prediction = model.predict(features)[0]
    
    if prediction == 1:
        return (0, 0, 255), f"🚨 **DANGER: MALICIOUS LINK DETECTED!**\n\nLINK: `{url}`", "error"
    else:
        return (0, 255, 0), f"✅ **SAFE WEBSITE**\n\nLINK: `{url}`", "success"

# --- UI HEADER ---
header_col1, header_col2 = st.columns([1, 5])
with header_col1:
    try:
        st.image("QG.png", width=90)
    except:
        st.write("🛡️") 
with header_col2:
    st.title("QGuard")
    st.caption("AI-Powered Phishing Defense System By Anushka Deshmukh")

# --- TABS FOR NAVIGATION ---
tab1, tab2 = st.tabs(["📸 Live Scanner", "✍️ Manual Link Checker"])

# === TAB 1: CAMERA SCANNER ===
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        run = st.checkbox('🔴 Start Camera', value=False)
    with col2:
        st.write(" **Status:** Ready")

    stframe = st.empty()
    result_area_camera = st.empty()

    if run:
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        
        while run:
            _, frame = cap.read()
            if frame is None:
                st.warning("Camera not accessible!")
                break

            frame = cv2.flip(frame, 1)
            data, bbox, _ = detector.detectAndDecode(frame)

            if bbox is not None and data:
                # Reuse the analysis logic
                color_bgr, msg, status_type = analyze_url(data)
                
                # Draw Box
                points = bbox.astype(int)
                for i in range(len(points[0])):
                    cv2.line(frame, tuple(points[0][i]), tuple(points[0][(i+1) % 4]), color_bgr, 5)

                # Show Result below video
                if status_type == "error":
                    result_area_camera.error(msg)
                elif status_type == "warning":
                    result_area_camera.warning(msg)
                else:
                    result_area_camera.success(msg)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, channels="RGB", use_container_width=True)

        cap.release()
    else:
        result_area_camera.info("👈 Click 'Start Camera' to begin scanning.")

# === TAB 2: MANUAL CHECKER ===
with tab2:
    st.subheader("Check a suspicious link manually")
    user_input = st.text_input("Paste URL here:", placeholder="Example: http://secure-login.paypal-manager.com")
    
    if st.button("Analyze Link 🔍"):
        if user_input:
            # Reuse the EXACT SAME AI BRAIN
            _, msg, status_type = analyze_url(user_input)
            
            if status_type == "error":
                st.error(msg)
            elif status_type == "warning":
                st.warning(msg)
            else:
                st.success(msg)
        else:
            st.info("Please enter a URL first.")