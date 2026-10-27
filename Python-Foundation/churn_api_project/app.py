import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Customer Churn Predictor", page_icon="📊", layout="centered"
)

st.title("📊 Enterprise Customer Churn Predictor")
st.markdown(
    "Enter a customer ID below to query the containerized FastAPI backend and check their subscription cancellation risk."
)

# Sidebar controls for authentication
st.sidebar.header("Authentication")
username_input = st.sidebar.text_input("Username", value="admin_user")

# Main input form
customer_id = st.text_input("Customer ID (e.g., 7590-VHVEG)", value="7590-VHVEG")

if st.button("Predict Churn Status", type="primary"):
    if not customer_id:
        st.warning("Please enter a valid Customer ID.")
    else:
        BASE_URL = "http://localhost:8000"

        try:
            with st.spinner("Authenticating with API..."):
                # 1. Get Token
                login_res = requests.post(
                    f"{BASE_URL}/login", params={"username": username_input}
                )

            if login_res.status_code == 200:
                token = login_res.json().get("access_token")

                with st.spinner(
                    "Analyzing customer data via Machine Learning model..."
                ):
                    # 2. Get Prediction
                    headers = {"token": token}
                    pred_res = requests.get(
                        f"{BASE_URL}/predict/{customer_id}", headers=headers
                    )

                if pred_res.status_code == 200:
                    data = pred_res.json()
                    will_churn = data.get("will_churn")

                    st.success("Prediction retrieved successfully!")

                    # Visual display card
                    if will_churn:
                        st.error(
                            f"⚠️ **High Risk**: Customer {customer_id} is **likely to churn**."
                        )
                    else:
                        st.info(
                            f"✅ **Low Risk**: Customer {customer_id} is **not likely to churn**."
                        )
                else:
                    st.error(f"API Error: {pred_res.text}")
            else:
                st.error(f"Authentication Failed: {login_res.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend API. Make sure your Docker containers are running!"
            )
