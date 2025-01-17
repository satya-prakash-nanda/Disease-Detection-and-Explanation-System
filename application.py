import streamlit as st
import requests

# API URL (change to your FastAPI server URL)
API_URL = "http://127.0.0.1:8000"

# Input fields
st.title("Disease Prediction and Explanation")
fever = st.selectbox("Fever", ["Yes", "No"])
cough = st.selectbox("Cough", ["Yes", "No"])
fatigue = st.selectbox("Fatigue", ["Yes", "No"])
difficulty_breathing = st.selectbox("Difficulty Breathing", ["Yes", "No"])
age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female"])
blood_pressure = st.selectbox("Blood Pressure", ["Normal", "High", "Low"])
cholesterol_level = st.selectbox("Cholesterol Level", ["Normal", "High", "Low"])

# Buttons
if st.button("Predict Disease"):
    # Prepare input data for prediction
    data = {
        "Fever": fever,
        "Cough": cough,
        "Fatigue": fatigue,
        "Difficulty_Breathing": difficulty_breathing,
        "Age": age,
        "Gender": gender,
        "Blood_Pressure": blood_pressure,
        "Cholesterol_Level": cholesterol_level,
    }

    # Send data to FastAPI's /predict endpoint
    response = requests.post(f"{API_URL}/predict", json=data)

    if response.status_code == 200:
        prediction = response.json().get("predicted_disease")
        st.session_state.predicted_disease = prediction  # Store prediction in session state
        st.success(f"Predicted Disease: {prediction}")
    else:
        st.error(f"Error: {response.text}")

if st.button("Explain Disease") and 'predicted_disease' in st.session_state:
    # Send request to explain the predicted disease
    predicted_disease = st.session_state.predicted_disease
    explanation_data = {"predicted_disease": predicted_disease}

    # Send data to FastAPI's /explain endpoint
    response = requests.post(f"{API_URL}/explain", json=explanation_data)

    if response.status_code == 200:
        explanation = response.json().get("explanation")
        st.write(explanation)  # Display the explanation
    else:
        st.error(f"Error: {response.text}")
