import cv2
import numpy as np
import pickle

# --- 1. LOAD THE BRAIN ---
print("Loading QGuard AI Model...")
try:
    with open("phishing_model.pkl", "rb") as file:
        model = pickle.load(file)
    print("✅ AI Model Loaded Successfully!")
except FileNotFoundError:
    print("❌ ERROR: 'phishing_model.pkl' not found.")
    exit()

# --- 2. DEFINE THE RULES ---
def get_features(url):
    url = str(url)
    return [
        len(url),                   
        url.count('.'),             
        url.count('@'),             
        url.count('-'),             
        1 if "https" in url else 0, 
        sum(c.isdigit() for c in url) 
    ]

# --- 3. THE WHITELIST (New Feature!) ---
def check_whitelist(url):
    # These are safe keywords for payments or common sites
    safe_keywords = ["upi://", "paytm", "phonepe", "gpay", "bhim", "google.com", "amazon"]
    
    for keyword in safe_keywords:
        if keyword.lower() in url.lower():
            return True # It is safe!
    return False # Not in whitelist, ask the AI

# --- 4. START THE SYSTEM ---
def start_qguard():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    # UI Colors
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    ORANGE = (0, 165, 255) # New color for Whitelisted items
    font = cv2.FONT_HERSHEY_SIMPLEX

    print("🛡️ QuishGuard Active. Point camera at a QR Code...")

    while True:
        _, frame = cap.read()
        
        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None and data:
            points = bbox.astype(int)
            
            # --- LOGIC START ---
            
            # STEP 1: Check Whitelist (Is it a Payment QR?)
            if check_whitelist(data):
                color = ORANGE
                text = "SAFE: PAYMENT/VERIFIED"
                print(f"Scanned: {data} -> [WHITELISTED SAFE]")
            
            # STEP 2: If not whitelisted, ask AI
            else:
                features = np.array([get_features(data)])
                prediction = model.predict(features)[0]
                
                if prediction == 1: 
                    color = RED
                    text = "DANGER: PHISHING!"
                else:
                    color = GREEN
                    text = "SAFE URL"
                print(f"Scanned: {data} -> {text}")

            # --- LOGIC END ---

            # Draw Box
            for i in range(len(points[0])):
                cv2.line(frame, tuple(points[0][i]), tuple(points[0][(i+1) % 4]), color, 5)
            
            # Draw Text
            cv2.rectangle(frame, (points[0][0][0], points[0][0][1] - 40), 
                                 (points[0][0][0] + 350, points[0][0][1]), color, -1)
            
            cv2.putText(frame, text, (points[0][0][0], points[0][0][1] - 10), 
                        font, 0.6, (255, 255, 255), 2)

        cv2.imshow('QuishGuard - Live Protection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    start_qguard()
