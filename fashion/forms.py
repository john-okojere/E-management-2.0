from django import forms
from .models import Inventory, Category

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['barcode','code','name','brand','category','size','quantity', 'cost_price','price','buying_unit','selling_unit','qty_per_buying_unit']

from .models import Day

class StartDayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['start_amount']

class EndDayForm(forms.Form):
    end_amount = forms.DecimalField(max_digits=15, decimal_places=2, label="End Amount")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']