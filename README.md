# 🩺 Disease Diagnosis and Explanation System

Welcome to the **Disease Diagnosis and Explanation System**! This project uses machine learning and natural language processing to predict diseases based on user inputs and provide detailed explanations for the predicted disease. 🌟

---

## 🚀 Features
- **Disease Prediction** 🧠  
  Predict diseases based on user inputs like symptoms, age, gender, blood pressure, and cholesterol level.
  
- **Disease Explanation** 📚  
  Get a detailed explanation of the predicted disease, including:
  - Symptoms
  - Causes
  - Treatments
  - Prevention tips

- **Interactive User Interface** 🖥️  
  A sleek Streamlit-powered frontend for user interaction.

- **REST API Integration** ⚙️  
  A FastAPI backend to handle predictions and explanations seamlessly.

---

## 🛠️ Technologies Used
- **Frontend**: [Streamlit](https://streamlit.io/) 🌐  
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) 🖧  
- **Machine Learning**: Scikit-learn, Pandas, Joblib 🤖  
- **NLP**: Hugging Face GPT-2 📝  
- **Other Tools**: NumPy, Requests, Pydantic ⚡

---

## 🧩 How It Works
1. **User Inputs**: Provide inputs such as symptoms, age, gender, etc., via the Streamlit app.
2. **Disease Prediction**: The backend predicts the disease using a trained machine learning model.
3. **Disease Explanation**: The predicted disease is sent to a Hugging Face GPT-2 model, which generates a detailed explanation.

---

## 📝 Installation Guide
Follow these steps to set up the project locally:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/satya-prakash-nanda/Disease-Detection-and-Explanation-System.git
   cd Disease-Detection-and-Explanation-System
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend Server**
   ```bash
   uvicorn app:app --reload
   ```
4. **Run the Streamlit Frontend**
   ```bash
   streamlit run application.py
   ```
