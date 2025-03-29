import os
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from statsmodels.tsa.arima.model import ARIMA

# Load model paths
MODEL_DIR = os.path.dirname(__file__)
ARIMA_MODEL_PATH = os.path.join(MODEL_DIR, "arima_model.pkl")
XGBOOST_MODEL_PATH = os.path.join(MODEL_DIR, "xgboost_model.pkl")
SALES_SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sales_scaler.pkl")

# Load trained models with error handling
def load_model(model_path):
    """Safely load a model and handle errors."""
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        print(f"⚠ Warning: Model not found at {model_path}. Ensure it's trained and saved properly.")
        return None

print("🔄 Loading trained models...")
arima_model = load_model(ARIMA_MODEL_PATH)
xgb_model = load_model(XGBOOST_MODEL_PATH)
sales_scaler = load_model(SALES_SCALER_PATH)
print("✅ Models loaded successfully!")


# Function to make predictions using ARIMA
def predict_arima(steps=12):
    if arima_model is None:
        print("❌ ARIMA model is missing. Please train it first.")
        return None

    print(f"📈 Predicting next {steps} months using ARIMA...")
    forecast = arima_model.forecast(steps=steps)

    #  Fix: Ensure predictions cannot be negative
    forecast = np.maximum(forecast, 0)

    return forecast


# Function to make predictions using XGBoost
def predict_xgboost(input_features):
    if xgb_model is None:
        print("❌ XGBoost model is missing. Please train it first.")
        return None

    input_df = pd.DataFrame([input_features], columns=[
        "Item_Identifier", "Item_Weight", "Item_Visibility", "Year", "Outlet_Identifier",
        "Item_Type", "Item_MRP", "MRP_Level", "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"
    ])

    print("🤖 Predicting sales using XGBoost...")
    prediction = xgb_model.predict(input_df)

    # Print raw predictions before scaling
    print(f"🔍 Raw XGBoost Prediction (Before Scaling): {prediction[0]}")

    # Ensure predictions are scaled back to original sales units
    if sales_scaler:
        try:
            print(f"🔍 Sales Scaler Min: {sales_scaler.data_min_}, Max: {sales_scaler.data_max_}")  # Debug
            prediction = sales_scaler.inverse_transform(prediction.reshape(-1, 1)).flatten()
        except Exception as e:
            print(f"⚠ Scaling error: {e}. Returning raw prediction.")

    # Print after inverse transform
    print(f"🔍 Scaled XGBoost Prediction (After Scaling): {prediction[0]}")

    # Ensure predictions are at least `0`
    prediction = np.maximum(prediction, 0)

    return prediction[0]


# Function to get user input for XGBoost predictions
def get_user_input():
    print("\n📊 Enter product details to predict sales:")
    try:
        input_features = {
            "Item_Identifier": float(input("🔹 Item Identifier (0-1 normalized): ")),
            "Item_Weight": float(input("🔹 Item Weight (0-1 normalized): ")),
            "Item_Visibility": float(input("🔹 Item Visibility (0-1 normalized): ")),
            "Year": int(input("🔹 Year for prediction (e.g., 2025): ")),
            "Outlet_Identifier": float(input("🔹 Outlet Identifier (0-1 normalized): ")),
            "Item_Type": float(input("🔹 Item Type (0-1 normalized): ")),
            "Item_MRP": float(input("🔹 Item MRP (0-1 normalized): ")),
            "MRP_Level": float(input("🔹 MRP Level (0-1 normalized): ")),
            "Outlet_Size": float(input("🔹 Outlet Size (0-1 normalized): ")),
            "Outlet_Location_Type": float(input("🔹 Outlet Location Type (0-1 normalized): ")),
            "Outlet_Type": float(input("🔹 Outlet Type (0-1 normalized): "))
        }
    except ValueError:
        print("❌ Invalid input! Please enter numeric values only.")
        return None

    return input_features
def predict_sales(input_data):
    """Predict sales using XGBoost model"""
    return predict_xgboost(input_data)


# Example: Predict next period's sales using both models
if __name__ == "__main__":
    print("🚀 Starting Sales Prediction...")

    # ARIMA Prediction
    steps = int(input("🔹 Enter number of months for ARIMA forecast: "))
    arima_forecast = predict_arima(steps=steps)
    if arima_forecast is not None:
        print("\n📊 ARIMA Forecast (Next {} months):".format(steps))
        print(arima_forecast)

    # XGBoost Prediction with User Input
    user_features = get_user_input()
    if user_features:
        xgb_forecast = predict_xgboost(user_features)
        print(f"\n🤖 XGBoost Prediction for {user_features['Year']}: {xgb_forecast:.2f} units")
