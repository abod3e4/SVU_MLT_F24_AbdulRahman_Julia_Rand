import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# المسارات
DATA_PATH = os.path.join('data', 'loan_prediction.csv')
MODEL_PATH = os.path.join('model', 'model.pkl')
ENCODERS_PATH = os.path.join('model', 'encoders.pkl')

def load_and_clean_data():
    df = pd.read_csv(DATA_PATH)

    # حذف الصفوف التي لا تحتوي على الحالة المستهدفة
    df = df[~df['Loan_Status'].isna()]

    # ملء القيم المفقودة بالقيم الشائعة أو المناسبة
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['Married'].fillna(df['Married'].mode()[0], inplace=True)
    df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
    df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
    df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
    df['Loan_Amount_Term'].fillna(360.0, inplace=True)
    df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)

    # 3. معالجة القيم الشاذة باستخدام IQR
    for col in ['LoanAmount', 'ApplicantIncome', 'CoapplicantIncome']:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df[col] = np.where(
                (df[col] < lower_bound) | (df[col] > upper_bound),
                df[col].median(),
                df[col]
            )

    return df

def preprocess_and_encode(df):
    df = df.copy()

    # إزالة الأعمدة غير المفيدة
    if 'Loan_ID' in df.columns:
        df.drop('Loan_ID', axis=1, inplace=True)

    # معالجة القيم في Dependents
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(int)

    # الأعمدة الفئوية التي تحتاج ترميز
    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status']
    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders

def train_and_save_model():
    df = load_and_clean_data()
    df_encoded, encoders = preprocess_and_encode(df)

    # تقسيم الميزات والهدف
    X = df_encoded.drop('Loan_Status', axis=1)
    y = df_encoded['Loan_Status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # تحديد وزن للفئات لمعالجة عدم التوازن
    class_weights = dict(pd.Series(y_train).value_counts(normalize=True))
    inv_weights = {cls: 1/w for cls, w in class_weights.items()}

    model = RandomForestClassifier(
        class_weight=inv_weights,
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    # حفظ النموذج والمشفرات
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)

    print("✅ النموذج والمشفرات تم حفظها بنجاح.")

if __name__ == "__main__":
    train_and_save_model()
