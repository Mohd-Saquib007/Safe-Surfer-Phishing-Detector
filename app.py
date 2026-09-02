from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import re
from urllib.parse import urlparse
import tldextract
import requests
from bs4 import BeautifulSoup
import whois
from datetime import datetime

app = Flask(__name__)
CORS(app) 

model = joblib.load('safe_surfer_model.pkl')
scaler = joblib.load('scaler.pkl')

def extract_features_from_url(url):
    # For now, let's return a dummy list of 30 features
    # Soon, we will replace this with real extraction logic
    return [1] * 30 

def get_features(url):
    features = []
    hostname = urlparse(url).netloc
    path = urlparse(url).path
    full_url = url.lower()
    
    # 1. IP Address
    features.append(-1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 1)
    # 2. URL Length
    features.append(1 if len(url) < 54 else (-1 if len(url) > 75 else 0))
    # 3. Shortening Service
    features.append(-1 if re.search('bit\.ly|goo\.gl|t\.co|tinyurl', url) else 1)
    # 4. @ Symbol
    features.append(-1 if "@" in url else 0)
    # 5. Double Slash Redirect
    features.append(-1 if url.rfind('//') > 7 else 1)
    # 6. Prefix-Suffix (Dash in domain) - Yahi ek pakad raha tha aapka model
    features.append(-1 if '-' in hostname else 1)
    # 7. Sub-domains
    dot_count = hostname.count('.')
    features.append(1 if dot_count <= 2 else (-1 if dot_count >= 4 else 0))
    # 8. SSL State
    features.append(1 if urlparse(url).scheme == 'https' else -1)
    # 9. Domain Registration Length (Simulation)
    features.append(-1 if len(hostname) > 20 else 1) 
    # 10. Favicon (External domain check)
    features.append(-1 if "favicon" in full_url and hostname not in full_url else 1)
    # 11. Port
    features.append(-1 if ":" in hostname and "443" not in hostname else 1)
    # 12. HTTPS Token in Hostname
    features.append(-1 if "https" in hostname else 1)
    
    # --- UCI Content Features (Simulating based on URL patterns) ---
    # 13. URL of Anchor (% of anchors leading to different domain)
    # Phishing sites often use '#' or different domains in links
    features.append(-1 if any(x in path for x in ['#', '.php', '.js', '.html']) else 1)
    
    # 14. Links in <Meta>, <Script> and <Link> tags
    features.append(-1 if path.count('/') > 3 else 1)
    
    # 15. SFH (Server Form Handler - empty or different domain)
    dangerous_keywords = ['login', 'sign', 'bank', 'secure', 'account', 'update', 'verify']
    features.append(-1 if any(k in full_url for k in dangerous_keywords) else 1)
    
    # 16. Submitting to Email
    features.append(-1 if "mail" in full_url else 1)
    
    # 17. Abnormal URL (Hostname not in path)
    features.append(-1 if hostname not in path and path != "" else 1)
    
    # 18. Redirects (Number of redirects)
    features.append(-1 if path.count('//') > 0 else 1)
    
    # --- Fill remaining features (To reach 30) ---
    # Agar 3+ danger signs hain, toh baaki features ko bhi suspicious (-1) kar do
    suspicion_score = sum(1 for f in features if f == -1)
    
    while len(features) < 30:
        if suspicion_score >= 3:
            features.append(-1)
        else:
            features.append(1)
            
    return features[:30]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    
    # 1. Feature Extraction
    raw_features = get_features(url)
    print(raw_features)
    # 2. Scaling
    final_features = scaler.transform([raw_features])
    # final_features = np.array(raw_features).reshape(1, -1)
    # 3. Get Probabilities instead of direct prediction
    # probabilities[0][0] -> Phishing (-1) ki probability
    # probabilities[0][1] -> Safe (1) ki probability
    probabilities = model.predict_proba(final_features)
    phishing_prob = probabilities[0][0]
    
    print(f"DEBUG - Phishing Probability: {phishing_prob * 100:.2f}%")

    # 4. Strict Threshold: Agar 20% bhi shak hai, toh phishing bolo
    # Standard 0.5 hota hai, hum 0.2 ya 0.3 use karenge security ke liye
    if phishing_prob > 0.4679: 
        result = "Phishing"
    else:
        result = "Safe"
    
    return jsonify({
        "url": url, 
        "result": result, 
        "probability": f"{phishing_prob * 100:.2f}%"
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)