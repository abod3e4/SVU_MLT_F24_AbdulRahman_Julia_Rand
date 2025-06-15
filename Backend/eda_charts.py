import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from services.request_store import load_requests

CHARTS_DIR = "static/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_charts():
    data = load_requests()
    if not data:
        return []

    df = pd.DataFrame(data)
    charts = []

    # 1. Distribution of predictions
    plt.figure(figsize=(5, 4))
    sns.countplot(x='prediction', data=df)
    plt.title("Prediction Distribution")
    path = os.path.join(CHARTS_DIR, "prediction_dist.png")
    plt.savefig(path)
    plt.close()
    charts.append("/static/charts/prediction_dist.png")

    # 2. Gender Distribution
    plt.figure(figsize=(5, 4))
    sns.countplot(x='Gender', data=df)
    plt.title("Gender Distribution")
    path = os.path.join(CHARTS_DIR, "gender_dist.png")
    plt.savefig(path)
    plt.close()
    charts.append("/static/charts/gender_dist.png")

    # 3. Income vs Loan Amount
    plt.figure(figsize=(6, 5))
    sns.scatterplot(x='ApplicantIncome', y='LoanAmount', hue='prediction', data=df)
    plt.title("Income vs Loan Amount")
    path = os.path.join(CHARTS_DIR, "income_loan.png")
    plt.savefig(path)
    plt.close()
    charts.append("/static/charts/income_loan.png")

    # 4. Request Count by Property Area
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Property_Area', data=df)
    plt.title("Requests by Property Area")
    path = os.path.join(CHARTS_DIR, "requests_by_area.png")
    plt.savefig(path)
    plt.close()
    charts.append("/static/charts/requests_by_area.png")

    # 5. Marital Status vs Prediction
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Married', hue='prediction', data=df)
    plt.title("Married vs Prediction")
    path = os.path.join(CHARTS_DIR, "married_vs_prediction.png")
    plt.savefig(path)
    plt.close()
    charts.append("/static/charts/married_vs_prediction.png")

    return charts
