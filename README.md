🛒 Sales Forecasting Web App using XGBoost and Django
A machine learning-powered web application that forecasts sales based on input features. The app is built with Django for the backend and uses XGBoost as the predictive model.

🚀 Features
Predicts sales using a trained XGBoost model

Interactive web interface with Django

Automatic feature importance visualization

Sales denormalization using saved scalers

Modern and responsive UI (can include Dark Knight background theme 😎)

🧠 Model
Model Used: XGBoost Regressor

Scaler: MinMaxScaler or StandardScaler (loaded from joblib)

Target: Item_Outlet_Sales

Features: Cleaned and encoded columns from the dataset

📁 Project Structure
sql
Copy
Edit
sales_forecasting/
├── app/
│   ├── templates/
│   │   └── view/
│   │       └── predict.html
│   ├── views.py
│   ├── urls.py
│   └── ...
├── static/
│   └── images/
│       └── dark_knight.jpg
├── model/
│   ├── xgboost_model.pkl
│   ├── sales_scaler.pkl
│   └── data.csv
├── train.py
├── utils.py
├── requirements.txt
└── README.md
⚙️ Setup Instructions
Clone the Repository

glone the repository
git clone https://github.com/yourusername/sales-forecasting-app.git
cd sales-forecasting-app



python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies


pip install -r requirements.txt
Train the Model

Make sure you have the dataset (e.g., sales_data.csv) and run:


python train.py
This will:

Clean the dataset

Train the XGBoost model

Save the model and scaler with joblib

Run the Server


python manage.py runserver
Then go to: http://127.0.0.1:8000/

🖼️ UI Customization
To change the background of the homepage:

html

<div class="container mt-5" style="background-image: url('/static/images/dark_knight.jpg'); background-size: cover; padding: 20px;">
📊 Output
Prediction Output: Displayed on predict.html

Model Evaluation: Mean Squared Error is printed after training

Top Features: Logged and printed during training

✅ Technologies Used
Python

Django

XGBoost

Pandas, NumPy

HTML/CSS (Bootstrap)

Joblib for saving models
