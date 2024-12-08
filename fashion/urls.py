from django.urls import path
from . import views

urlpatterns = [
    path('cashier/', views.cashier, name='fashion_cashier'),
    path('start_day/', views.start_day, name='fashion_start_day'),
    path('end_day/', views.end_day, name='fashion_end_day'),
    path('end_of_day_report/', views.end_of_day_report, name='fashion_end_of_day_report'),

    #Inventory
    path('inventory/', views.inventory_list, name='fashion_inventory_list'),
    path('inventory/category', views.create_category, name='fashion_inventory_categorry'),
    path('inventory/add/', views.add_inventory, name='fashion_add_inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name='fashion_update_inventory'),
    path('inventory/delete/<int:pk>/', views.delete_inventory, name='fashion_delete_inventory'),

    #sales
    path('create-sale/', views.create_sale, name='fashion_create_sale'),
    path('add-sale-item/', views.add_sale_item, name='fashion_add_sale_item'),
    path('complete-sale/', views.complete_sale, name='fashion_complete_sale'),
    path('Pay-for-sale/', views.pay_for_sale, name='fashion_pay_for_sale'),
    path('sale/<int:sale_id>/receipt/', views.sale_receipt, name='fashion_sale_receipt'),

    
    #discount
    path('apply-sale-item-discount/', views.apply_sale_item_discount, name='fashion_apply_sale_item_discount'),
    path('create-sale-discount/', views.apply_sale_discount, name='fashion_apply_sale_discount'),

    #history
    path('sales-history/', views.sales_history, name='fashion_sales_history'),
    path('fetch-sales-data/', views.fetch_sales_data, name='fashion_fetch_sales_data'),

    #Report
    path('audit-report/', views.audit_report, name='fashion_audit_report'),
    path('end-of-day-report/', views.end_of_day_report, name='fashion_end_of_day_report'),
    path('api/sales/', views.fetch_eod_sales_data, name='fashion_fetch_sales_data'),

    path('make-payment/', views.make_payment, name='fashion_make_payment'),
]
