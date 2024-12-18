from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='fashion_dashboard'),
    path('cashier/', views.cashier, name='fashion_cashier'),
    path('start_day/', views.start_day, name='fashion_start_day'),
    path('end_day/', views.end_day, name='fashion_end_day'),
    path('end_of_day_report/', views.end_of_day_report, name='fashion_end_of_day_report'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/doc/', views.export_doc, name='export_doc'),

    #sales
    path('create-sale/', views.create_sale, name='fashion_create_sale'),
    path('add-sale-item/', views.add_sale_item, name='fashion_add_sale_item'),
    path('complete-sale/', views.complete_sale, name='fashion_complete_sale'),
    path('Pay-for-sale/', views.pay_for_sale, name='fashion_pay_for_sale'),
    path('sale/receipt/<int:sale_id>/', views.sale_receipt, name='fashion_sale_receipt'),

   
    #Inventory
    path('inventory/', views.inventory_list, name='fashion_inventory_list'),
    path('inventory/category', views.create_category, name='fashion_inventory_categorry'),
    path('inventory/add/', views.add_inventory, name='fashion_add_inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name='fashion_update_inventory'),
    path('inventory/delete/<int:pk>/', views.delete_inventory, name='fashion_delete_inventory'),

     
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

   
    # Approvals
    path("manage-approvals/", views.manage_approvals, name="fashion_manage_approvals"),
    path("approve-day/<int:day_id>/", views.approve_day, name="fashion_approve_day"),
    path("approve-discount/<int:discount_id>/", views.approve_discount, name="fashion_approve_discount"),

    # Newly Added URLs
    # Sales Reports
    path('daily-sales-report/', views.daily_sales_report, name='daily_sales_report'),
    path('weekly-sales-report/', views.weekly_sales_report, name='weekly_sales_report'),
    path('monthly-sales-report/', views.monthly_sales_report, name='monthly_sales_report'),
    path('sales-by-staff/', views.sales_by_staff_report, name='sales_by_staff_report'),
    path('sales-by-product/', views.sales_by_product_report, name='sales_by_product_report'),

    # Inventory Reports
    path('low-stock-report/', views.low_stock_report, name='low_stock_report'),
    path('inventory-turnover-report/', views.inventory_turnover_report, name='inventory_turnover_report'),

    # Financial Reports
    path('daily-cashflow-report/', views.daily_cashflow_report, name='daily_cashflow_report'),
    path('sales-tax-report/', views.sales_tax_report, name='sales_tax_report'),

    # Discounts and Refunds
    path('discounts-report/', views.discounts_report, name='discounts_report'),
    path('refunds-report/', views.refunds_report, name='refunds_report'),

    # API Endpoints
    path('api/sales-growth/', views.api_sales_growth, name='api_sales_growth'),
    path('api/sales-performance/', views.api_sales_performance, name='api_sales_performance'),
    path('api/sales-by-product/', views.api_sales_by_product, name='api_sales_by_product'),
    path('api/payment-summary/', views.api_payment_summary, name='api_payment_summary'),

    path('upload-inventory/', views.upload_inventory, name='fashion_upload_inventory'),
    path('api/inventory/', views.inventory_list_api, name='inventory_list_api'),
    
    # Inventory Adjustment
    path('quantity-increase/<int:sale_item_id>/', views.increase_quantity, name='fashion_increase_quantity'),
    path('quantity-decrease/<int:sale_item_id>/', views.decrease_quantity, name='fashion_decrease_quantity'),
      path('update-sale-item/<int:sale_item_id>/', views.update_sale_item, name='update_sale_item'),
    path('remove-sale-item/<int:sale_item_id>/', views.remove_sale_item, name='remove_sale_item'),

]
 