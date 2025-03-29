from django import forms
from .models import SalesRecord

class SalesForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = '__all__'
