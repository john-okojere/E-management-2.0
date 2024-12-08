from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Inventory
from .forms import InventoryForm, StartDayForm, EndDayForm, CategoryForm
from users.models import CustomUser
from .models import Day, Category

from .forms import StartDayForm

@login_required
def start_day(request):
    # Check if there is any day that has not ended
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    if unfinished_day:
            return redirect('spa_cashier')

    if request.method == 'POST':
        form = StartDayForm(request.POST)
        if form.is_valid():
            day = form.save(commit=False)
            day.staff = request.user
            day.start_time = datetime.now().time()
            day.save()
            return redirect('spa_cashier')
    else:
        form = StartDayForm()

    return render(request, 'spa/start_day.html', {'form': form})


@login_required
def cashier(request):
    # Check if there is any day that has not ended
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    if not unfinished_day:
        return redirect('spa_start_day')  # Redirect to the start day view if no day has started

    items = Inventory.objects.all()
    cat = Category.objects.all()
    context = {
        'items': items,
        'categories': cat,
    }
    return render(request, 'spa/pos.html', context)

@login_required
def add_inventory(request):
    # Check if the user has an associated staff profile
    try:
        user = request.user
    except AttributeError:
        messages.error(request, "You don't have permission to upload inventory.")
        return redirect('spa_inventory_list')

    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            inventory_item = form.save(commit=False)
            # Associate the logged-in staff with the inventory
            inventory_item.staff = user
            inventory_item.save()
            messages.success(request, "Inventory item added successfully!")
            return redirect('spa_inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'spa/inventory/add.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spa_inventory_list')
    else:
        form = CategoryForm()
    return render(request, 'spa/inventory/add.html', {'form': form})

def inventory_list(request):
    items = Inventory.objects.all().order_by('-date')
    return render(request, 'spa/inventory/list.html', {'items': items})


# Update Inventory View
def update_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # Respond to AJAX request with success message
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "Inventory item updated successfully!"})
            messages.success(request, "Inventory item updated successfully!")
            return redirect('spa_inventory_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = InventoryForm(instance=item)
    return render(request, 'spa/inventory/update_inventory.html', {'form': form})


# Delete Inventory View
def delete_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        item.delete()
        # Respond to AJAX request with success message
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Inventory item deleted successfully!"})
        messages.success(request, "Inventory item deleted successfully!")
        return redirect('spa_inventory_list')
    return render(request, 'spa/inventory/delete_inventory.html', {'item': item})


from django.http import JsonResponse
from .models import Sale, SaleItem, Inventory

def create_sale(request):
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    if request.method == 'POST':
        cashier_id = request.user.id
        total_amount = request.POST.get('total_amount')
        cashier = CustomUser.objects.get(id=cashier_id)
        sale = Sale.objects.create(cashier=cashier, total=total_amount, day=unfinished_day)
        return JsonResponse({'status': 'success', 'sale_id': sale.id})

from django.db.models import F

def add_sale_item(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        total = quantity * price

        # Fetch the sale and product
        sale = Sale.objects.get(id=sale_id)
        product = Inventory.objects.get(id=product_id)

        # Create the sale item
        sale_item = SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price=price,
            total=total
        )

        # Update the sale total
        updated_total = SaleItem.objects.filter(sale=sale).aggregate(total_sum=Sum('total'))['total_sum'] or 0
        sale.total = updated_total
        sale.save(update_fields=['total'])

        # Refresh the sale object to get the updated total
        sale.refresh_from_db()

        return JsonResponse({
            'status': 'success',
            'sale_item_id': sale_item.id,
            'updated_sale_total': float(sale.total)
        })
def complete_sale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        print(sale_id)
        
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.completed = True
            sale.save()
            
            return JsonResponse({'status': 'success', 'message': 'Sale marked as completed.'})
        except Sale.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sale not found.'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Sale, SaleItem, SaleDiscount, SaleItemDiscount, CustomUser

def apply_sale_discount(request):
    if request.method == 'POST':
        cashier = request.user
        sale_id = request.POST.get('sale_id')
        proposed_discount = request.POST.get('proposed_discount')

        sale = get_object_or_404(Sale, id=sale_id)

        # Create SaleDiscount
        SaleDiscount.objects.create(
            cashier=cashier,
            sale=sale,
            proposed_discount=proposed_discount,
        )

        return JsonResponse({'success': True, 'message': 'Sale discount created successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def apply_sale_item_discount(request):
    if request.method == 'POST':
        cashier = request.user
        sale_item_id = request.POST.get('sale_item_id')
        proposed_discount = request.POST.get('proposed_discount')

        sale_item = get_object_or_404(SaleItem, id=sale_item_id)

        # Create SaleItemDiscount
        SaleItemDiscount.objects.create(
            cashier=cashier,
            sale=sale_item,
            proposed_discount=proposed_discount,
        )

        return JsonResponse({'success': True, 'message': 'Sale item discount created successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

from django.db.models import Sum
from django.db.models.functions import TruncDay

def sales_history(request):
    # Filter completed sales
    sales = Sale.objects.filter(completed=True).order_by('-date')
    if request.user.role == "cashier":
        sales = Sale.objects.filter(completed=True, cashier= request.user).order_by('-date')
    sales_data = []

    # Sales data for table
    for sale in sales:
        sales_data.append({
            'id': sale.id,
            'cashier': sale.cashier.username,
            'total': float(sale.total),
            'date': sale.date.strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Summarize sales by date for the graph
    graph_data = (
        Sale.objects.filter(completed=True)
        .annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total=Sum('total'))
        .order_by('day')
    )

    # Convert graph data into labels and values
    graph_labels = [entry['day'].strftime('%Y-%m-%d') for entry in graph_data]
    graph_values = [float(entry['total']) for entry in graph_data]

    if request.is_ajax():
        return JsonResponse({'sales': sales_data, 'graph_labels': graph_labels, 'graph_values': graph_values})
    return render(request, 'spa/sales_history.html', {
        'sales': sales_data,
        'graph_labels': graph_labels,
        'graph_values': graph_values,
    })

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import Sum
def sales_history(request):
    # Check user role and permissions
    if request.user.role == "Cashier":
        sales = Sale.objects.filter(completed=True, cashier=request.user)
    elif request.user.level >= 3:
        sales = Sale.objects.filter(completed=True)
    else:
        sales = Sale.objects.none()  # Return no sales if the user doesn't have the right access level

    sales_data = []
    # Prepare sales data for rendering or JSON response
    for sale in sales:
        sales_data.append({
            'id': sale.id,
            'cashier': sale.cashier.username,  # Assuming cashier has a related `user` object
            'total': float(sale.total),
            'completed': 'Yes' if sale.completed else 'No',
            'paid': 'Yes' if sale.paid else 'No',
            'date': sale.date.strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Check if the request is an AJAX call and return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'sales': sales_data})

    # For regular GET requests, render the page
    return render(request, 'spa/sales_history.html', {
        'sales': sales_data,
    })


from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncDay
from .models import Sale

def fetch_sales_data(request):
    if request.method == 'GET':
        # Aggregate sales data
        graph_data = (
            Sale.objects.filter(completed=True)
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(total=Sum('total'))
            .order_by('day')
        )

        graph_labels = [entry['day'].strftime('%Y-%m-%d') for entry in graph_data]
        graph_values = [float(entry['total']) for entry in graph_data]

        return JsonResponse({
            'graph_labels': graph_labels,
            'graph_values': graph_values,
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


from django.shortcuts import render
from django.http import JsonResponse
from .models import Sale  # Replace with your actual model for transactions
from django.db.models import Sum, Count
import datetime



# Generate a custom report (optional extension for downloadable formats like PDF/Excel)
def custom_report(request):
    # Handle filters and dynamic reports (e.g., by cashier, status, date, etc.)
    # Return processed data for export
    return JsonResponse({'status': 'Custom report generation in progress...'})


from django.shortcuts import render
from django.http import JsonResponse
from .models import Sale, Payment  # Assuming you have a Sale model for storing sales data
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, F
from decimal import Decimal

def end_of_day_report(request):
    # Fetch the day's data
    day = Day.objects.filter(staff=request.user, end=False).first()
    if not day:
        return JsonResponse({"error": "Day not found or not ended"}, status=404)

    sales = Sale.objects.filter(day=day)
    payments = Payment.objects.filter(sale__in=sales)

    # Calculate totals
    total_sales = sales.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    completed_sales = sales.filter(completed=True).count()
    pending_sales = sales.filter(completed=False).count()
    total_discounts = SaleDiscount.objects.filter(sale__in=sales, approved=True).aggregate(total=Sum('proposed_discount'))['total'] or Decimal('0.00')

    # Payment breakdown
    cash_payments = payments.filter(payment_type='cash').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    card_payments = payments.filter(payment_type='card').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    transfer_payments = payments.filter(payment_type='transfer').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    expected_cash_at_hand = day.start_amount + cash_payments

    # Category-wise sales
    category_sales = (
        SaleItem.objects.filter(sale__in=sales)
        .values(category=F('product__category__name'))
        .annotate(total_revenue=Sum('total'), items_sold=Sum('quantity'))
        .order_by('-total_revenue')
    )

    # Top products
    top_products = (
        SaleItem.objects.filter(sale__in=sales)
        .values(product_name=F('product__name'))
        .annotate(total_revenue=Sum('total'), quantity_sold=Sum('quantity'))
        .order_by('-quantity_sold')[:5]
    )

    # Prepare report data
    report = {
        "overview": {
            "date": day.date.strftime('%Y-%m-%d'),
            "cashier": day.staff.username,
            "start_time": day.start_time,
            "end_time": day.end_time,
            "starting_amount": float(day.start_amount),
            "ending_amount": float(day.end_amount) if day.end_amount else None,
            "total_sales": float(total_sales),
            "completed_sales": completed_sales,
            "pending_sales": pending_sales,
        },
        "payments": {
            "cash": float(cash_payments),
            "card": float(card_payments),
            "transfer": float(transfer_payments),
            "expected_cash_at_hand": float(expected_cash_at_hand),
        },
        "discounts": {
            "total_discounts": float(total_discounts),
        },
        "category_sales": list(category_sales),
        "top_products": list(top_products),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX requests
        return JsonResponse(report)

    return render(request, 'spa/end-of-day.html', {'report': report})


import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Payment

@csrf_exempt
def make_payment(request):
    if request.method == "POST":
        data = request.POST
        sale_id = data.get("sale_id")
        amount = data.get("amount")
        payment_method = data.get("payment_method")
        paid_by = data.get("paid_by")

        # For card payments, expect additional data
        if payment_method == "card":
            payment_id = uuid.uuid4().hex
            # Call Paystack API here to verify payment
            # Add your Paystack verification logic (e.g., check transaction ID)
        else:
            payment_id = None
        sale = Sale.objects.get(id = sale_id)
        # Save payment record
        payment = Payment.objects.create(
            sale = sale,
            cashier = request.user,
            amount=amount,
            payment_type=payment_method,
            paid_by=paid_by,
            payment_id=payment_id,
        )
        payment.save()

        return JsonResponse({"status": "success", "payment_id": payment.id})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def pay_for_sale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
                
        try:
            sale = Sale.objects.get(id=sale_id)
            sale.paid = True
            sale.save()
            
            return JsonResponse({'status': 'success', 'message': 'Sale marked as completed.'})
        except Sale.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sale not found.'})

def sale_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_items = sale.items.all()

    receipt_data = {
        "id": sale.id,
        "cashier": sale.cashier.username,  # Adjust as necessary
        "date": sale.date.strftime("%Y-%m-%d %H:%M:%S"),
        "total": sale.total,
        "items": [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "total": item.total
            }
            for item in sale_items
        ]
    }
    print(receipt_data)
    return JsonResponse(receipt_data)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from .models import Sale
from datetime import datetime

# API to fetch sales data
@require_GET
def fetch_eod_sales_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    # Check if the cashier has ended the day
    if not request.user.CustomUser.has_ended_day:
        return JsonResponse({"error": "End of day process not completed."}, status=403)

    # Filter sales for today
    today = datetime.now().date()
    sales = Sale.objects.filter(date__date=today)
    
    data = [
        {
            "id": sale.id,
            "cashier": str(sale.cashier),
            "total": float(sale.total),
            "completed": "Yes" if sale.completed else "No",
            "paid": float(sale.paid),
            "date": sale.date.strftime("%Y-%m-%d %H:%M:%S"),
            "payment_method": sale.payment_method if hasattr(sale, 'payment_method') else "N/A",
        }
        for sale in sales
    ]
    return JsonResponse(data, safe=False)

# API to end the day
def end_day(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    if not unfinished_day:
        return redirect('spa_start_day')  # Redirect to the start day view if no day has started
    
    unfinished_day.end_time  = datetime.now().time()
    unfinished_day.end = True
    unfinished_day.no_of_sales = Sale.objects.filter(day = unfinished_day).count()
    unfinished_day.end_amount = Sale.objects.filter(day = unfinished_day).aggregate(Sum('total'))['total__sum']
    unfinished_day.save()
    return redirect('spa_end_of_day_report')  # Redirect to the start day view if no day has started

# Reset 'end day' status at midnight (Optional: handled via management command or cron job)

def audit_report(request):
    # Aggregate data
    total_sales = Sale.objects.filter(completed=True).aggregate(total=Sum('total'))['total'] or 0
    total_items_sold = SaleItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
    inventory_data = Inventory.objects.all()
    sales_per_day = (
        Sale.objects.filter(completed=True)
        .values('date__date')
        .annotate(total_sales=Sum('total'))
        .order_by('-date__date')
    )

    # Data for charts
    inventory_chart_data = {
        "labels": [item.name for item in inventory_data],
    }

    sales_chart_data = {
        "labels": [str(day['date__date']) for day in sales_per_day],
        "values": [float(day['total_sales']) for day in sales_per_day],
    }

    context = {
        "total_sales": total_sales,
        "total_items_sold": total_items_sold,
        "inventory_data": inventory_data,
        "sales_per_day": sales_per_day,
        "inventory_chart_data": inventory_chart_data,
        "sales_chart_data": sales_chart_data,
    }
    return render(request, "spa/audit_report.html", context)