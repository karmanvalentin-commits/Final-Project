"""
Навчання моделі (це той самий код, що й у ноутбуці, але у вигляді окремого скрипта).
Запускається один раз: python train_model.py
Результат - файл loan_model.joblib, який використовує сайт.
Модель навчається саме на вашому комп'ютері, щоб версії бібліотек збігалися з тими, що працюють у Django.
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("loan_data.csv")
data = df.drop(columns=["Loan_ID"])
X = data.drop(columns=["Loan_Status"])
y = data["Loan_Status"].map({"Y": 1, "N": 0})

# розділення 80 / 20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

numeric_features = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History"]
categorical_features = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
])

models = {
    "KNN": (KNeighborsClassifier(),
            {"model__n_neighbors": [3, 5, 7, 9, 11, 15], "model__weights": ["uniform", "distance"]}),
    "Decision Tree": (DecisionTreeClassifier(random_state=42),
                      {"model__max_depth": [2, 3, 4, 5, 7, None], "model__min_samples_leaf": [1, 5, 10, 20]}),
    "Random Forest": (RandomForestClassifier(random_state=42),
                      {"model__n_estimators": [100, 200], "model__max_depth": [3, 5, 8, None],
                       "model__min_samples_leaf": [1, 5, 10]}),
}

best_name, best_model, best_acc = None, None, -1
for name, (clf, params) in models.items():
    pipe = Pipeline([("preprocess", preprocessor), ("model", clf)])
    grid = GridSearchCV(pipe, params, cv=5, scoring="accuracy", n_jobs=-1)
    grid.fit(X_train, y_train)
    acc = accuracy_score(y_test, grid.best_estimator_.predict(X_test))
    print(f"{name}: accuracy на тесті = {acc:.3f}")
    if acc > best_acc:
        best_name, best_model, best_acc = name, grid.best_estimator_, acc

joblib.dump(best_model, "loan_model.joblib")
print(f"\nНайкраща модель: {best_name} ({best_acc:.3f}). Збережено у loan_model.joblib")

# --- Самоперевірка: модель має реагувати на кредитну історію ---
check = {
    "Gender": "Male", "Married": "Yes", "Dependents": "0", "Education": "Graduate", "Self_Employed": "No",
    "ApplicantIncome": 4000, "CoapplicantIncome": 1500, "LoanAmount": 120, "Loan_Amount_Term": 360,
    "Property_Area": "Urban",
}
good = best_model.predict_proba(pd.DataFrame([dict(check, Credit_History=1.0)]))[0][1] * 100
bad = best_model.predict_proba(pd.DataFrame([dict(check, Credit_History=0.0)]))[0][1] * 100
print(f"Перевірка: хороша кредитна історія -> {good:.0f}%, погана -> {bad:.0f}%")
if abs(good - bad) < 5:
    print("УВАГА: модель не реагує на кредитну історію. Напишіть про це, ми розберемось.")
else:
    print("Все гаразд: модель реагує на кредитну історію.")
