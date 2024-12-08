from django import forms
from .models import Inventory, Category

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'barcode' ,'icon','price', 'description','category']

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