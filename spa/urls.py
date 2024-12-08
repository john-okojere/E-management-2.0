from django.urls import path
from . import views

urlpatterns = [
    path('cashier/', views.cashier, name='spa_cashier'),
    path('start_day/', views.start_day, name='spa_start_day'),
    path('end_day/', views.end_day, name='spa_end_day'),
    path('end_of_day_report/', views.end_of_day_report, name='spa_end_of_day_report'),

    #Inventory
    path('inventory/', views.inventory_list, name='spa_inventory_list'),
    path('inventory/category', views.create_category, name='spa_inventory_categorry'),
    path('inventory/add/', views.add_inventory, name='spa_add_inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name='spa_update_inventory'),
    path('inventory/delete/<int:pk>/', views.delete_inventory, name='spa_delete_inventory'),

    #sales
    path('create-sale/', views.create_sale, name='spa_create_sale'),
    path('add-sale-item/', views.add_sale_item, name='spa_add_sale_item'),
    path('complete-sale/', views.complete_sale, name='spa_complete_sale'),
    path('Pay-for-sale/', views.pay_for_sale, name='spa_pay_for_sale'),
    path('sale/<int:sale_id>/receipt/', views.sale_receipt, name='spa_sale_receipt'),

    
    #discount
    path('apply-sale-item-discount/', views.apply_sale_item_discount, name='spa_apply_sale_item_discount'),
    path('create-sale-discount/', views.apply_sale_discount, name='spa_apply_sale_discount'),

    #history
    path('sales-history/', views.sales_history, name='spa_sales_history'),
    path('fetch-sales-data/', views.fetch_sales_data, name='spa_fetch_sales_data'),

    #Report
    path('audit-report/', views.audit_report, name='spa_audit_report'),
    path('end-of-day-report/', views.end_of_day_report, name='spa_end_of_day_report'),
    path('api/sales/', views.fetch_eod_sales_data, name='spa_fetch_sales_data'),

    path('make-payment/', views.make_payment, name='spa_make_payment'),
]
