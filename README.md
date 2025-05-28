<h1 align="center">🛒 Sales Forecasting Web App</h1>
<p align="center">
  <em>A machine learning-powered web application that forecasts sales using XGBoost and Django</em>
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li><strong>ML-Powered:</strong> Predicts sales using a trained <code>XGBoost Regressor</code></li>
  <li><strong>Django Web App:</strong> Backend powered by Django framework</li>
  <li><strong>Feature Importance:</strong> Auto-generated plots of feature impact</li>
  <li><strong>Sales Denormalization:</strong> Uses pre-saved <code>scalers</code> to return original sales values</li>
  <li><strong>Modern UI:</strong> Responsive interface (supports Dark Knight theme 😎)</li>
</ul>

<hr>

<h2>🧠 Model Details</h2>

<ul>
  <li><strong>Model:</strong> XGBoost Regressor</li>
  <li><strong>Scaler:</strong> MinMaxScaler or StandardScaler (via <code>joblib</code>)</li>
  <li><strong>Target:</strong> <code>Item_Outlet_Sales</code></li>
  <li><strong>Features:</strong> Encoded and cleaned dataset columns</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
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
</pre>

<hr>

<h2>⚙️ Setup Instructions</h2>

<ol>
  <li><strong>Clone the Repository</strong>
    <pre><code>git clone https://github.com/yourusername/sales-forecasting-app.git
cd sales-forecasting-app</code></pre>
  </li>

  <li><strong>Create & Activate Virtual Environment (optional)</strong>
    <pre><code>python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate</code></pre>
  </li>

  <li><strong>Install Dependencies</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li><strong>Run the App</strong>
    <pre><code>python manage.py runserver</code></pre>
    Visit: <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a>
  </li>
</ol>

<hr>

<h2>🖼️ UI Preview</h2>

<p align="center">
  <img src="Screenshot 2025-05-28 092520.png" alt="Dark Knight UI" width="500">
   <img src="Screenshot 2025-05-28 092555.png" alt="Dark Knight UI" width="500">
   <img src="Screenshot 2025-05-28 092630.png" alt="Dark Knight UI" width="500">
</p>

<hr>

<h2>🤝 Contributing</h2>

<p>Pull requests are welcome! For major changes, open an issue to discuss what you'd like to improve.</p>

<hr>


<h2>📬 Contact</h2>

<p>
  📧 Email: <a href="mailto:shubhrai598@gmail.com">shubhrai598@gmail.com</a><br>
  💻 GitHub: <a href="https://github.com/shubh-gitpush" target="_blank">github.com/shubh-gitpush</a>
</p>
