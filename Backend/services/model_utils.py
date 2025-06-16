import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join('model', 'model.pkl')
ENCODERS_PATH = os.path.join('model', 'encoders.pkl')

# تحميل النموذج والمشفرات
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODERS_PATH)

def preprocess_input_data(df):
    # تعويض القيم المفقودة
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['Married'].fillna(df['Married'].mode()[0], inplace=True)
    df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
    df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
    df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
    df['Loan_Amount_Term'].fillna(360.0, inplace=True)
    df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)

    # تحويل Dependents من '3+' إلى 3
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(int)

    # تشفير باستخدام المشفرات المحفوظة
    for col, le in encoders.items():
        if col != 'Loan_Status':  # لا نشفر الهدف
            df[col] = le.transform(df[col])

    # إزالة العمود غير المفيد
    if 'Loan_ID' in df.columns:
        df.drop(['Loan_ID'], axis=1, inplace=True)

    return df

def predict(input_dict):
    df = pd.DataFrame([input_dict])  # تحويل إلى DataFrame
    df = preprocess_input_data(df)   # معالجة البيانات
    prediction = model.predict(df)   # التنبؤ
    return prediction[0]             # إرجاع النتيجة


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

def get_model_metrics():
    # تحميل البيانات
    df = pd.read_csv(os.path.join('data', 'loan_prediction.csv'))

    # تعويض القيم المفقودة
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['Married'].fillna(df['Married'].mode()[0], inplace=True)
    df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
    df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
    df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
    df['Loan_Amount_Term'].fillna(360.0, inplace=True)
    df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
    
    # حذف الصفوف بدون Loan_Status
    df = df[~df['Loan_Status'].isna()]

    # تحويل Dependents من '3+' إلى 3
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(int)

    # تشفير باستخدام المشفرات المحفوظة
    for col, le in encoders.items():
        df[col] = le.transform(df[col])

    # إزالة العمود غير المفيد
    if 'Loan_ID' in df.columns:
        df.drop(['Loan_ID'], axis=1, inplace=True)

    # فصل الميزات عن الهدف
    X = df.drop('Loan_Status', axis=1)
    y = df['Loan_Status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    y_pred = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred)
    }

def predict_with_probability(input_dict):
    df = pd.DataFrame([input_dict])
    df = preprocess_input_data(df)

    proba = model.predict_proba(df)[0]  # إرجاع [prob_rejected, prob_approved]
    prediction = model.predict(df)[0]   # النتيجة النهائية (مقبول/مرفوض)

    prob_approved = float(proba[1])  # تحويل إلى float بايثون
    prediction_label = str(prediction)  # تحويل إلى str بايثون

    return {
        "prediction": prediction_label,
        "approval_probability": round(prob_approved * 100, 2)  # كنسبة مئوية
    }


