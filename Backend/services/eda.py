import pandas as pd
from services.request_store import load_requests

def generate_eda_summary():
    data = load_requests()
    if not data:
        return {"message": "No data available"}

    df = pd.DataFrame(data)

    summary = {}

    # تحويل أنواع البيانات إلى Python native types
    summary["total_requests"] = int(len(df))

    summary["prediction_distribution"] = {
        str(k): int(v) for k, v in df["prediction"].value_counts().items()
    }

    summary["average_loan_amount"] = round(float(df["LoanAmount"].mean()), 2)
    summary["average_applicant_income"] = round(float(df["ApplicantIncome"].mean()), 2)

    summary["gender_distribution"] = {
        str(k): int(v) for k, v in df["Gender"].value_counts().items()
    }

    summary["area_distribution"] = {
        str(k): int(v) for k, v in df["Property_Area"].value_counts().items()
    }

    summary["married_distribution"] = {
        str(k): int(v) for k, v in df["Married"].value_counts().items()
    }

    return summary

import os

# def analyze_data_issues():
#     file_path = os.path.join('data', 'loan_prediction.csv')
#     try:
#         df = pd.read_csv(file_path)
#     except Exception as e:
#         return {"error": f"Failed to read dataset: {e}"}

#     issues = {}

#     # 1. القيم المفقودة
#     missing = df.isnull().sum()
#     missing = missing[missing > 0]
#     if not missing.empty:
#         issues["missing_values"] = missing.to_dict()

#     # 2. القيم الشاذة
#     outliers = {}

#     if 'LoanAmount' in df.columns:
#         outliers['LoanAmount_zero_or_negative'] = int((df['LoanAmount'] <= 0).sum())

#     if 'Loan_Amount_Term' in df.columns:
#         outliers['Loan_Amount_Term_out_of_range'] = int(((df['Loan_Amount_Term'] < 12) | (df['Loan_Amount_Term'] > 600)).sum())

#     if outliers:
#         issues["outliers"] = outliers

#     # 3. القيم المكررة
#     duplicate_count = df.duplicated().sum()
#     if duplicate_count > 0:
#         issues["duplicate_rows"] = int(duplicate_count)

#     return {"data_issues_report": issues}


import pandas as pd
import os

import pandas as pd
import numpy as np
import os

def analyze_data_issues():
    file_path = os.path.join('data', 'loan_prediction.csv')
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {"error": f"Failed to read dataset: {e}"}

    report = {
        "initial_issues": {},
        "fixes_applied": {},
        "final_notes": []
    }

    # --- 1. Missing Values ---
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        report["initial_issues"]["missing_values"] = missing.to_dict()

        fix_notes = {}
        for col in missing.index:
            if col == 'LoanAmount':
                df[col].fillna(df[col].median(), inplace=True)
                fix_notes[col] = "Filled with median"
            elif col == 'Loan_Amount_Term':
                df[col].fillna(360.0, inplace=True)
                fix_notes[col] = "Filled with default value 360.0"
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
                fix_notes[col] = "Filled with mode"

        report["fixes_applied"]["missing_values_fixes"] = fix_notes

    # --- 2. Outliers ---
    outliers_info = {}
    fixes_info = {}

    # معالجة القيم الشاذة في LoanAmount باستخدام IQR
    if 'LoanAmount' in df.columns:
        Q1 = df['LoanAmount'].quantile(0.25)
        Q3 = df['LoanAmount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_count = ((df['LoanAmount'] < lower_bound) | (df['LoanAmount'] > upper_bound)).sum()
        if outlier_count > 0:
            outliers_info['LoanAmount'] = int(outlier_count)
            df['LoanAmount'] = df['LoanAmount'].apply(
                lambda x: df['LoanAmount'].median() if x < lower_bound or x > upper_bound else x
            )
            fixes_info['LoanAmount'] = "Outliers replaced with median using IQR method"

    # معالجة القيم الشاذة في Loan_Amount_Term
    if 'Loan_Amount_Term' in df.columns:
        out_of_range_count = ((df['Loan_Amount_Term'] < 12) | (df['Loan_Amount_Term'] > 600)).sum()
        if out_of_range_count > 0:
            outliers_info['Loan_Amount_Term'] = int(out_of_range_count)
            df['Loan_Amount_Term'] = df['Loan_Amount_Term'].apply(
                lambda x: 360.0 if x < 12 or x > 600 else x
            )
            fixes_info['Loan_Amount_Term'] = "Values out of range replaced with 360.0"

    # معالجة القيم الشاذة في ApplicantIncome باستخدام IQR
    if 'ApplicantIncome' in df.columns:
        Q1 = df['ApplicantIncome'].quantile(0.25)
        Q3 = df['ApplicantIncome'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_count = ((df['ApplicantIncome'] < lower_bound) | (df['ApplicantIncome'] > upper_bound)).sum()
        if outlier_count > 0:
            outliers_info['ApplicantIncome'] = int(outlier_count)
            df['ApplicantIncome'] = df['ApplicantIncome'].apply(
                lambda x: df['ApplicantIncome'].median() if x < lower_bound or x > upper_bound else x
            )
            fixes_info['ApplicantIncome'] = "Outliers replaced with median using IQR method"

    # معالجة القيم الشاذة في CoapplicantIncome باستخدام IQR
    if 'CoapplicantIncome' in df.columns:
        Q1 = df['CoapplicantIncome'].quantile(0.25)
        Q3 = df['CoapplicantIncome'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_count = ((df['CoapplicantIncome'] < lower_bound) | (df['CoapplicantIncome'] > upper_bound)).sum()
        if outlier_count > 0:
            outliers_info['CoapplicantIncome'] = int(outlier_count)
            df['CoapplicantIncome'] = df['CoapplicantIncome'].apply(
                lambda x: df['CoapplicantIncome'].median() if x < lower_bound or x > upper_bound else x
            )
            fixes_info['CoapplicantIncome'] = "Outliers replaced with median using IQR method"

    if outliers_info:
        report["initial_issues"]["outliers"] = outliers_info
        report["fixes_applied"]["outliers_fixed"] = fixes_info

    # --- 3. Duplicate Rows ---
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        report["initial_issues"]["duplicate_rows"] = int(duplicate_count)
        df.drop_duplicates(inplace=True)
        report["fixes_applied"]["duplicates_removed"] = int(duplicate_count)

    # --- 4. Final Notes ---
    report["final_notes"].append("All detected issues have been fixed according to data cleaning strategy.")
    report["final_notes"].append(f"Final dataset shape: {df.shape}")

    return report



