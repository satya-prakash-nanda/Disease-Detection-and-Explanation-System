from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import requests
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Load the trained model pipeline and label encoder for disease prediction
pipeline = joblib.load('disease_prediction_model.pkl')  # Adjust this path as needed
label_encoder = joblib.load('label_encoder.pkl')  # Adjust this path as needed

# Hugging Face API configuration
HUGGINGFACE_API_KEY = "your_api_key"
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"


# Define the input data model for disease prediction
class InputData(BaseModel):
    Fever: str
    Cough: str
    Fatigue: str
    Difficulty_Breathing: str
    Age: int
    Gender: str
    Blood_Pressure: str
    Cholesterol_Level: str

# Define the input data model for disease explanation
class DiseaseInput(BaseModel):
    predicted_disease: str

# Define the predict endpoint
@app.post("/predict")
async def predict_disease(data: InputData):
    try:
        # Convert the input data to a DataFrame
        new_input = {
            'Fever': [data.Fever],
            'Cough': [data.Cough],
            'Fatigue': [data.Fatigue],
            'Difficulty Breathing': [data.Difficulty_Breathing],
            'Age': [data.Age],
            'Gender': [data.Gender],
            'Blood Pressure': [data.Blood_Pressure],
            'Cholesterol Level': [data.Cholesterol_Level]
        }

        new_input_df = pd.DataFrame(new_input)

        # Manually encode the binary columns ('Yes'/'No' to 1/0)
        binary_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
        new_input_df[binary_columns] = new_input_df[binary_columns].applymap(lambda x: 1 if x == 'Yes' else 0)

        # Ensure all columns required by the model are present
        required_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing', 'Age', 'Gender', 'Blood Pressure',
                            'Cholesterol Level']
        for col in required_columns:
            if col not in new_input_df.columns:
                new_input_df[col] = [None]  # Add missing column with NaN or appropriate default value

        # Make the prediction using the trained model pipeline
        prediction = pipeline.predict(new_input_df)

        # Decode the prediction from numerical label to the original class name
        predicted_disease = label_encoder.inverse_transform(prediction)

        return {"predicted_disease": predicted_disease[0]}

    except Exception as e:
        return {"error": str(e)}

# Define the explain endpoint
@app.post("/explain")
async def explain_disease(data: DiseaseInput):
    try:
        # Prepare the Hugging Face API request payload
        explanation_prompt = f"Please provide a brief explanation of the disease '{data.predicted_disease}', including symptoms, causes, treatments, and prevention tips."


        payload = {
            "inputs": explanation_prompt,
            "parameters": {
                "max_length": 200,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }

        # Make the API request
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(HUGGINGFACE_API_URL, json=payload, headers=headers)

        # Check for errors in the response
        if response.status_code != 200:
            return {"error": f"Hugging Face API error: {response.status_code} - {response.text}"}

        # Parse the Hugging Face API response
        response_data = response.json()

        # Check if the response contains the expected generated text
        explanation = ""
        if isinstance(response_data, list) and len(response_data) > 0:
            explanation = response_data[0].get("generated_text", "").strip()

        # Post-process the explanation (if necessary)
        if not explanation:
            explanation = "I'm sorry, I couldn't generate a detailed response. Please try again with a different disease name."

        # Return the explanation
        return {
            "predicted_disease": data.predicted_disease,
            "explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}


