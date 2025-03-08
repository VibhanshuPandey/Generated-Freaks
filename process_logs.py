import pandas as pd
import json
import requests

# Replace with your Gemini API key
API_KEY = "API key"
API_URL = f"api url"

# Read and combine CSV files
support_logs = pd.read_csv("data/support_logs.csv")
shipping_logs = pd.read_csv("data/shipping_logs.csv")
logs = pd.concat([support_logs, shipping_logs], ignore_index=True)

# Calculate metrics
avg_response_time = logs["response_time"].mean()
avg_confidence = logs["confidence"].mean()
low_confidence_queries = logs[logs["confidence"] < 85]

# Prepare metrics for JSON
metrics = {
    "order_tracking": {
        "avg_response_time": round(avg_response_time, 2),
        "avg_confidence": round(avg_confidence, 2)
    }
}

# Generate suggestion using Gemini API
low_confidence_text = "\n".join(low_confidence_queries["query"].tolist())
prompt = f"Given these low-confidence queries:\n{low_confidence_text}\nSuggest an improvement for the system."
payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}
headers = {"Content-Type": "application/json"}

response = requests.post(API_URL, json=payload, headers=headers)
if response.status_code == 200:
    suggestion = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
else:
    suggestion = "Error calling Gemini API: " + response.text

# Save outputs
with open("analytics.json", "w") as f:
    json.dump({"metrics": metrics}, f)
with open("suggestions.json", "w") as f:
    json.dump({"suggestion": suggestion}, f)

print("Metrics and suggestions generated!")