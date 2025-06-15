import joblib
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = os.path.join("model", "model.pkl")

# نفس الأعمدة التي دربنا بها النموذج
label_encoders = {
    'Gender': LabelEncoder().fit(['Female', 'Male']),
    'Married': LabelEncoder().fit(['No', 'Yes']),
    'Education': LabelEncoder().fit(['Graduate', 'Not Graduate']),
    'Self_Employed': LabelEncoder().fit(['No', 'Yes']),
    'Property_Area': LabelEncoder().fit(['Rural', 'Semiurban', 'Urban']),
}

model = joblib.load(MODEL_PATH)

def preprocess_input(data):
    encoded = [
        label_encoders['Gender'].transform([data.Gender])[0],
        label_encoders['Married'].transform([data.Married])[0],
        int(data.Dependents.replace("+", "")),
        label_encoders['Education'].transform([data.Education])[0],
        label_encoders['Self_Employed'].transform([data.Self_Employed])[0],
        data.ApplicantIncome,
        data.CoapplicantIncome,
        data.LoanAmount,
        data.Loan_Amount_Term,
        data.Credit_History,
        label_encoders['Property_Area'].transform([data.Property_Area])[0],
    ]
    return np.array(encoded).reshape(1, -1)

def predict_loan_status(request):
    X = preprocess_input(request)
    prediction = model.predict(X)[0]
    return "Approved" if prediction == 1 else "Rejected"
