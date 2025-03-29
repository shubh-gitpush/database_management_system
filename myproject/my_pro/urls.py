from django.urls import path
from .views import sales_dashboard
from .views import predict_view
from .views import add_sales_record
from .views import home

urlpatterns = [
    path('sales/', sales_dashboard, name='sales_dashboard'),
    path('predict/', predict_view, name='predict_view'),
    path('dashboard/', sales_dashboard, name='sales_dashboard'),
    path('add-sales/', add_sales_record, name="add_sales"),
    path('',home,name="home")
]