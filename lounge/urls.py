from django.urls import path
from . import views

urlpatterns = [
    path('cashier/', views.cashier, name='lounge_cashier'),
    path('start_day/', views.start_day, name='lounge_start_day'),
    path('end_day/', views.end_day, name='lounge_end_day'),
    path('end_of_day_report/', views.end_of_day_report, name='lounge_end_of_day_report'),

    #Inventory
    path('inventory/', views.inventory_list, name='lounge_inventory_list'),
    path('inventory/category', views.create_category, name='lounge_inventory_categorry'),
    path('inventory/add/', views.add_inventory, name='lounge_add_inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name='lounge_update_inventory'),
    path('inventory/delete/<int:pk>/', views.delete_inventory, name='lounge_delete_inventory'),

    #sales
    path('create-sale/', views.create_sale, name='lounge_create_sale'),
    path('add-sale-item/', views.add_sale_item, name='lounge_add_sale_item'),
    path('complete-sale/', views.complete_sale, name='lounge_complete_sale'),
    path('Pay-for-sale/', views.pay_for_sale, name='lounge_pay_for_sale'),
    path('sale/<int:sale_id>/receipt/', views.sale_receipt, name='lounge_sale_receipt'),

    
    #discount
    path('apply-sale-item-discount/', views.apply_sale_item_discount, name='lounge_apply_sale_item_discount'),
    path('create-sale-discount/', views.apply_sale_discount, name='lounge_apply_sale_discount'),

    #history
    path('sales-history/', views.sales_history, name='lounge_sales_history'),
    path('fetch-sales-data/', views.fetch_sales_data, name='lounge_fetch_sales_data'),

    #Report
    path('audit-report/', views.audit_report, name='lounge_audit_report'),
    path('end-of-day-report/', views.end_of_day_report, name='lounge_end_of_day_report'),
    path('api/sales/', views.fetch_eod_sales_data, name='lounge_fetch_sales_data'),

    path('make-payment/', views.make_payment, name='lounge_make_payment'),
]
