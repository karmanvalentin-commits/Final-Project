"""Тут Django-сайт використовує навчену модель машинного навчання (файл loan_model.joblib)."""
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "loan_model.joblib"


def predict(data):
    """
    data - словник з даними форми.
    Повертає: (схвалено True/False, імовірність у %, що саме отримала модель, назва моделі).
    """
    # Назви колонок мають бути ТАКИМИ САМИМИ, як у loan_data.csv, бо на них навчалась модель
    inputs = {
        "Gender": data["gender"],
        "Married": data["married"],
        "Dependents": data["dependents"],
        "Education": data["education"],
        "Self_Employed": data["self_employed"],
        "ApplicantIncome": int(data["applicant_income"]),
        "CoapplicantIncome": int(data["coapplicant_income"]),
        "LoanAmount": int(data["loan_amount"]),
        "Loan_Amount_Term": int(data["loan_amount_term"]),
        "Credit_History": float(int(data["credit_history"])),
        "Property_Area": data["property_area"],
    }
    row = pd.DataFrame([inputs])

    # Модель завантажується при кожному запиті (файл маленький), щоб ніколи не користуватись застарілою
    model = joblib.load(MODEL_PATH)
    approved = bool(model.predict(row)[0] == 1)
    probability = round(float(model.predict_proba(row)[0][1]) * 100, 1)
    model_name = type(model.named_steps["model"]).__name__
    return approved, probability, inputs, model_name
