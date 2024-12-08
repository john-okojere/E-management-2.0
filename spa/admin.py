from django.contrib import admin
from .models import Inventory, Sale, SaleItem, Receipt, SaleDiscount, SaleItemDiscount, Day, Payment

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'staff', 'date')
    list_filter = ('date', 'staff')
    search_fields = ('name', 'description', 'staff__username')
    ordering = ('-date',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'total')
    readonly_fields = ('total',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cashier', 'total', 'date')
    list_filter = ('date', 'cashier__username')
    search_fields = ('cashier__username', 'id')
    ordering = ('-date',)
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity', 'price', 'total')
    list_filter = ('sale__date', 'product__name')
    search_fields = ('sale__id', 'product__name')
    ordering = ('-sale__date',)

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'sale', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('receipt_number', 'sale__id')
    ordering = ('-created_at',)

@admin.register(SaleDiscount)
class SaleDiscountAdmin(admin.ModelAdmin):
    list_display = ('sale', 'cashier', 'proposed_discount', 'approved', 'approved_by')
    list_filter = ('approved', 'cashier__username', 'sale__date')
    search_fields = ('sale__id', 'cashier__username')
    ordering = ('-sale__date',)

@admin.register(SaleItemDiscount)
class SaleItemDiscountAdmin(admin.ModelAdmin):
    list_display = ('sale', 'cashier', 'proposed_discount', 'approved', 'approved_by')
    list_filter = ('approved', 'cashier__username', 'sale__sale__date')
    search_fields = ('sale__sale__id', 'cashier__username')
    ordering = ('-sale__sale__date',)

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_amount', 'end_amount', 'start_time', 'end_time', 'no_of_sales', 'date')
    list_filter = ('staff', 'date')
    search_fields = ('staff__username', 'start_amount', 'end_amount')

admin.site.register(Payment)