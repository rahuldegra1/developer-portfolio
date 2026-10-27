import requests

BASE_URL = "http://127.0.0.1:8000"
CUSTOMER_ID = "7590-VHVEG"

# 1. Authenticate to get the JWT token
print("1. Requesting authentication token...")
login_response = requests.post(f"{BASE_URL}/login", params={"username": "admin_user"})

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"   Success! Token received: {token[:20]}...")

    # 2. Pass the token securely in the headers to get a prediction
    print(f"\n2. Requesting churn prediction for customer {CUSTOMER_ID}...")
    headers = {"token": token}
    predict_response = requests.get(
        f"{BASE_URL}/predict/{CUSTOMER_ID}", headers=headers
    )

    if predict_response.status_code == 200:
        result = predict_response.json()
        print("   Prediction received from API:")
        print(f"   --> Customer: {result['customer_id']}")
        print(f"   --> Will Churn: {result['will_churn']}")
    else:
        print(f"   Error querying prediction endpoint: {predict_response.text}")
else:
    print(f"   Error logging in: {login_response.text}")
