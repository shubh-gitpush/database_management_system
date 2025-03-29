import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os
import joblib


# Function to Load and Clean Data
def load_and_clean_data(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print("❌ File not found! Please check the path:", file_path)
        return None, None, None
    else:
        print("✅ File found, proceeding to load...")

    # Load dataset
    try:
        df = pd.read_csv(file_path)
        print("✅ File loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None, None, None

    # Remove missing values
    df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # ✅ Fix: Ensure "Year" has correct values
    if "Outlet_Establishment_Year" in df.columns:
        df["Year"] = df["Outlet_Establishment_Year"]  # Use actual establishment year if available

    if "Year" in df.columns:
        df["Year"] = df["Year"].apply(lambda x: x + 2000 if x < 50 else x)  # Convert 2-digit years
        df["Year"] = df["Year"].astype(int)  # Ensure integer type

    # Encode categorical data
    categorical_cols = df.select_dtypes(include=['object']).columns
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Normalize numerical data (EXCLUDING "Year")
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if "Year" in numerical_cols:
        numerical_cols.remove("Year")  # Ensure "Year" is not scaled

    # Apply MinMaxScaler to numerical columns
    scaler = MinMaxScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # ✅ Apply a separate MinMaxScaler for Sales
    if "Item_Outlet_Sales" in df.columns:
        sales_scaler = MinMaxScaler()
        df["Item_Outlet_Sales"] = sales_scaler.fit_transform(df[["Item_Outlet_Sales"]])

        # Save the sales scaler for later inverse transformations
        scaler_path = os.path.join(os.path.dirname(file_path), "sales_scaler.pkl")
        joblib.dump(sales_scaler, scaler_path)
        print(f"✅ Sales scaler saved at {scaler_path}")

    print("✅ Data preprocessing complete! First 5 rows:")
    print(df.head())

    return df, label_encoders, scaler


# Run function only if script is executed directly
if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Bigbazaar_sales_data.csv")

    print("🚀 Starting Data Preprocessing...")
    df_cleaned, label_encoders, scaler = load_and_clean_data(file_path)

    if df_cleaned is not None:
        print("✅ Preprocessing Successful! First 5 rows shown above.")
        print("Unique Years:", df_cleaned["Year"].unique())  # Verify Year column
    else:
        print("❌ Data preprocessing failed.")
