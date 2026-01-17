# 🛡️ QGuard: AI-Powered QR Phishing Defense System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Prototype-green)

**QGuard** is a real-time cybersecurity tool designed to detect and block **"Quishing"** (QR Code Phishing) attacks. It uses a **Hybrid Intelligence System** combining Machine Learning (Random Forest) with rule-based whitelisting to verify QR codes before the user opens them.

---

## 🚨 The Problem
QR codes are everywhere—payments, menus, and logins. However, humans cannot read QR codes, making them a perfect vehicle for cyberattacks. Hackers embed malicious URLs inside QR codes, bypassing traditional email filters.

## 💡 The Solution
QuishGuard acts as a "security guard" between the camera and the browser. It scans the QR code, analyzes the URL structure using AI, and provides an instant safety rating:
* 🟢 **Green:** Safe Website.
* 🟠 **Orange:** Verified Payment (UPI, GPay, Paytm).
* 🔴 **Red:** Danger / Malicious Phishing Pattern.

---

## ✨ Key Features
* **📸 Real-Time Scanning:** Live video feed detection using OpenCV.
* **🧠 AI Analysis:** A Random Forest Classifier trained on 15,000+ malicious and benign URLs.
* **✅ Payment Whitelist:** Frictionless verification for trusted payment apps (`upi://`, `gpay`, `paytm`).
* **🛡️ Hybrid Detection:** Combines AI probability with rigid "Blacklist Rules" to catch specific threats like `verify-account` or `update-password`.
* **✍️ Manual Link Checker:** A dedicated tab to manually paste and analyze suspicious SMS/Email links.
* **🔒 Privacy First:** Runs 100% offline. No data leaves your device.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Interface:** Streamlit (Web UI)
* **Computer Vision:** OpenCV (`cv2`)
* **Machine Learning:** Scikit-Learn (`sklearn`)
* **Data Handling:** Pandas & Numpy

---

## 📂 Dataset & Model Info
The AI model (`phishing_model.pkl`) is included in this repository, so the application runs out-of-the-box.

However, the training dataset (`data.csv`) is **not included** due to GitHub's file size limits. If you wish to retrain the model yourself:
1.  Download the dataset from Kaggle: **[Phishing Site URLs Dataset](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls)**.
2.  Rename the downloaded file to `data.csv`.
3.  Place it in the project folder.
4.  Run `python train_model.py`.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/CodeWhizAnu/QGuard.git] (https://github.com/CodeWhizAnu/QGuard.git))
cd QuishGuard-QR-Security

```

### 2. Install Dependencies

You can install all required libraries with this single command:

```bash
pip install streamlit opencv-python pandas scikit-learn numpy

```

### 3. Run the Application

Start the Streamlit server:

```bash
streamlit run app.py

```

*The application will open automatically in your default web browser.*

---

## 📖 How It Works

1. **Input:** The system captures a QR code via webcam or accepts a manual URL input.
2. **Step 1 (Whitelist Check):** It checks if the link is a known payment provider (e.g., `upi://`). If yes  **Safe (Orange)**.
3. **Step 2 (Blacklist Trap):** It checks for obvious phishing keywords (e.g., `secure-login`, `verify-bank`). If found  **Danger (Red)**.

4. **Step 3 (AI Prediction):** If the link is unknown, the AI model analyzes 6 structural features:
* URL Length
* Count of Dots (.)
* Count of Hyphens (-)
* Presence of '@' symbol
* HTTPS check
* Numeric character ratio


5. **Output:** The user receives a clear visual alert (Green/Orange/Red).

---

## 🔮 Future Scope

* **Mobile App:** Convert the logic into a native Android/iOS app using Flutter or Kivy.
* **API Integration:** Connect with Google Safe Browsing API for double-verification.
* **Browser Extension:** A plugin to auto-scan QR images on websites.

---

## 👨‍💻 Author

Built by **[Anushka Deshmukh]**.

```


```
