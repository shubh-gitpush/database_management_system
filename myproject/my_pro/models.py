from django.db import models

class SalesRecord(models.Model):
        item_name = models.CharField(max_length=100,default=0.0)
        item_weight = models.FloatField(default=0.0)
        item_visibility = models.FloatField(default=0.0)
        item_mrp = models.FloatField(default=0.0)  # ✅ Add default value
        outlet_size = models.CharField(max_length=50,default=0.0)
        outlet_location_type = models.CharField(max_length=50,default=0.0)
        outlet_type = models.CharField(max_length=50,default=0.0)
        sales_amount = models.FloatField(default=0.0)
        date = models.DateField(auto_now_add=True)

        def __str__(self):
            return f"{self.item_name} - {self.sales_amount}"
