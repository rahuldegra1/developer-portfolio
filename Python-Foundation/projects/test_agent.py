import requests

# 1. Point to your active local Jev microservice
SERVER_URL = "http://localhost:8000/v1/choice"

# 2. Prepare the ticket or log data you want to process
data_payload = {
    "state": "The user is requesting an instant refund because their subscription was renewed by mistake.",
    "options": ["refund_queue", "technical_glitch", "general_inquiry"],
}

print("🤖 Sending routing payload to local server...")

# 3. Hit the endpoint and collect the instant decision matrix
response = requests.post(SERVER_URL, json=data_payload)
decision = response.json()

# 4. Use the results in your app code
winning_choice = decision["choice"]
confidence_score = decision["confidence"]

print(
    f"✅ Target Route Identified: {winning_choice} ({confidence_score:.1%} confidence)"
)

# Example deterministic execution logic based on your local engine
if winning_choice == "refund_queue" and confidence_score > 0.80:
    print("🚀 Triggering automated Stripe backend validation pipeline...")
