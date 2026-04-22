# **Safe-Surfer: AI-Powered Phishing Detection System**

Safe-Surfer is a real-time cybersecurity tool designed to protect users from malicious phishing websites. It consists of a Brave/Chrome Extension frontend and a Flask-based Machine Learning backend trained on the UCI Phishing Website Dataset.

## **Features**

**Deep Feature Extraction:** Extracts 30 technical parameters from any URL (Structural, Content, and Behavioral).   
**AI-Driven Analysis:** Uses a Random Forest Classifier to predict the legitimacy of a site.   
**Real-time Protection:** Scans URLs instantly through a browser extension.   
**Probability-Based Scoring:** Implements a strict security threshold to catch even the most sophisticated "zero-day" phishing links.   

## **Tech Stack**

**Backend:** Python, Flask, Gunicorn   
**Machine Learning:** Scikit-learn, Joblib, Pandas, NumPy   
**Frontend:** JavaScript (Web Extensions API), HTML, CSS   
**Deployment:** Vercel / Render   

## **How It Works**

**Input:** The browser extension captures the current tab's URL.   
**Processing:** The URL is sent to the Flask API.   
**Extraction:** The backend runs a get_features() script to convert the URL into a numerical vector of 30 features (e.g., SSL state, prefix-suffix in domain, anchor URLs).   
**Prediction:** The pre-trained model analyzes the vector and returns a probability score.   
**Alert:** If the phishing probability exceeds the threshold, the extension alerts the user.   

## **Project Structure**

Plaintext   
├── backend/   
│   ├── app.py                  # Flask API with Feature Extraction Logic   
│   ├── safe_surfer_model.pkl   # Pre-trained Random Forest Model   
│   ├── scaler.pkl              # StandardScaler for feature normalization   
│   ├── requirements.txt        # Python dependencies   
│   └── vercel.json             # Deployment configuration   
└── extension/   
    ├── manifest.json           # Extension configuration   
    ├── popup.html              # Extension UI   
    └── popup.js                # Frontend logic for API communication   

## Installation & Setup

1. Setup Backend   
    - **Clone the repository**   
    ``git clone https://github.com/YOUR_USERNAME/Safe-Surfer.git``

    - **Navigate to backend**   
    ``cd backend``

    - **Install dependencies**   
    ``pip install -r requirements.txt``

    - **Run the server**   
    ``python app.py``

2. Setup Extension
    + Open Brave/Chrome and go to brave://extensions (or chrome://extensions).   
    + Enable Developer Mode (top right).   
    + Click Load unpacked and select the extension/ folder from this project.   
    + Ensure the API_URL in popup.js matches your running backend.   

## Model Performance

- The model is trained on the UCI Phishing Dataset consisting of 11,000+ samples.   
- Algorithm: Random Forest Classifier   
- Classes: Legitimate (1) vs. Phishing (-1)   
- Optimization: Balanced class weights and customized probability thresholds for enhanced security.   

## License   
Distributed under the MIT License. See LICENSE for more information.
