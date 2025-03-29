# views.py
from django.shortcuts import render
from .models import SalesRecord
from .ml_models.predictions import predict_sales  # Import prediction function
from .forms import SalesForm
from django.shortcuts import redirect

def sales_dashboard(request):
    """Display past sales data in the dashboard."""
    sales_data = SalesRecord.objects.all()  # Fetch sales data from DB
    return render(request, 'view/sales_dashboard.html', {'sales_data': sales_data})

def add_sales_record(request):
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')  # Redirect after submission
    else:
        form = SalesForm()

    return render(request, 'view/add_sales.html', {'form': form})

def predict_view(request):
    """Handle sales predictions using the trained model."""
    prediction = None  # Default value

    if request.method == 'POST':
        # Get input data from form submission
        input_data = {
            'Item_Weight': float(request.POST['weight']),
            'Item_Visibility': float(request.POST['visibility']),
            'Item_MRP': float(request.POST['mrp']),
            'Outlet_Size': float(request.POST['outlet_size']),
            'Outlet_Location_Type': float(request.POST['location']),
            'Outlet_Type': float(request.POST['outlet_type']),
        }

        # Call the prediction function
        prediction = predict_sales(input_data)

    return render(request, 'view/predict.html', {'prediction': prediction})

def home(request):
    return render(request,'view/home.html')
