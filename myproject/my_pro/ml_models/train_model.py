import os
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from my_pro.ml_models.preprocess import load_and_clean_data

# Define paths for saving models
MODEL_DIR = os.path.dirname(__file__)
ARIMA_MODEL_PATH = os.path.join(MODEL_DIR, "arima_model.pkl")
XGBOOST_MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.pkl")
SALES_SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sales_scaler.pkl")

# Ensure the directory exists
os.makedirs(MODEL_DIR, exist_ok=True)


# Function to check & make data stationary
def make_stationary(series):
    if series.isnull().all() or series.empty:
        raise ValueError("❌ Sales series is empty after preprocessing! Check for missing values.")

    result = adfuller(series.dropna())  # Drop NaN before ADF test
    p_value = result[1]

    if p_value > 0.05:
        print("⚠ Data is not stationary, applying differencing...")
        stationary_series = series.diff().dropna()

        if stationary_series.empty:
            raise ValueError("❌ Differencing resulted in an empty series! Cannot proceed with ARIMA.")

        return stationary_series
    else:
        print("✅ Data is already stationary.")
        return series


# Function to train ARIMA model
def train_arima_model(file_path):
    df, _, _ = load_and_clean_data(file_path)

    if "Year" not in df.columns:
        raise ValueError("❌ 'Year' column not found in dataset!")

    df["Year"] = pd.to_datetime(df["Year"], format="%Y", errors="coerce")
    df.dropna(subset=["Year"], inplace=True)
    df.set_index("Year", inplace=True)

    sales_series = df["Item_Outlet_Sales"].resample("M").sum()

    # Make data stationary
    sales_series = make_stationary(sales_series)

    print("📊 Training ARIMA model...")
    arima_model = ARIMA(sales_series, order=(1, 1, 1))  # (p,d,q) values adjusted
    arima_fit = arima_model.fit()

    joblib.dump(arima_fit, ARIMA_MODEL_PATH)
    print(f"✅ ARIMA model saved at {ARIMA_MODEL_PATH}")

    return arima_fit


# Function to train XGBoost model
def train_xgboost_model(file_path):
    df, _, _ = load_and_clean_data(file_path)

    # Load sales scaler
    if os.path.exists(SALES_SCALER_PATH):
        sales_scaler = joblib.load(SALES_SCALER_PATH)
        print("✅ Sales scaler loaded successfully.")
    else:
        print("⚠ Warning: Sales scaler not found!")
        sales_scaler = None

    # Define features and target
    X = df.drop(columns=['Item_Outlet_Sales', 'Converted Sales'], errors='ignore')
    y = df['Item_Outlet_Sales']

    # Split into training & testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=None, shuffle=True
    )

    print("🚀 Training XGBoost model...")
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, reg_lambda=1)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # ✅ Fix: Use `sales_scaler` for denormalization
    if sales_scaler:
        y_test_actual = sales_scaler.inverse_transform(y_test.values.reshape(-1, 1)).flatten()
        predictions_actual = sales_scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
    else:
        y_test_actual = y_test.values
        predictions_actual = predictions

    # Compute MSE again
    print("🔍 y_test_actual (first 5):", y_test_actual[:5])
    print("🔍 predictions_actual (first 5):", predictions_actual[:5])
    mse = mean_squared_error(y_test_actual, predictions_actual)
    print(f"📉 XGBoost Model MSE: {mse:.10f}")

    # Save the trained XGBoost model
    joblib.dump(model, XGBOOST_MODEL_PATH)
    print(f"✅ XGBoost model saved at {XGBOOST_MODEL_PATH}")

    # 🔍 Feature Importance Analysis
    feature_importance = model.feature_importances_
    feature_names = X.columns
    importance_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importance})
    importance_df = importance_df.sort_values(by="Importance", ascending=False)

    print("\n🔍 Top Features in XGBoost Model:")
    print(importance_df.head(10))  # Print top 10 features

    return model


# Function to train the Hybrid ARIMA + XGBoost model
def train_hybrid_model(file_path):
    print("🔹 Training ARIMA model...")
    train_arima_model(file_path)

    print("🔹 Training XGBoost model...")
    train_xgboost_model(file_path)

    print("🚀 Hybrid ARIMA + XGBoost Model Training Completed!")


# Run the script
if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Bigbazaar_sales_data.csv")
    train_hybrid_model(file_path)
