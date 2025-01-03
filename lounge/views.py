from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Inventory, Category
from .forms import InventoryForm, StartDayForm, EndDayForm, CategoryForm
from users.models import CustomUser
from .models import Day

from .forms import StartDayForm

@login_required
def start_day(request):
    # Check if there is any day that has not ended
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    if unfinished_day:
            return redirect('lounge_cashier')

    if request.method == 'POST':
        form = StartDayForm(request.POST)
        if form.is_valid():
            day = form.save(commit=False)
            day.staff = request.user
            day.start_time = datetime.now().time()
            day.save()
            return redirect('lounge_cashier')
    else:
        form = StartDayForm()

    return render(request, 'lounge/start_day.html', {'form': form})


@login_required
def cashier(request):
    # Check if there is any day that has not ended
    unfinished_day = Day.objects.filter(staff=request.user, end=False).first()
    print(unfinished_day,'jkn')

    if not unfinished_day:
        return redirect('lounge_start_day')  # Redirect to the start day view if no day has started

    items = Inventory.objects.all()
    category = Category.objects.all()
    context = {
        'items': items,
        'category': category,
    }
    return render(request, 'lounge/pos.html', context)

@login_required
def add_inventory(request):
    # Check if the user has an associated staff profile
    try:
        user = request.user
    except AttributeError:
        messages.error(request, "You don't have permission to upload inventory.")
        return redirect('lounge_inventory_list')

    if request.method == "POST":
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            inventory_item = form.save(commit=False)
            # Associate the logged-in staff with the inventory
            inventory_item.staff = user
            print(inventory_item)
            inventory_item.save()
            messages.success(request, "Inventory item added successfully!")
            return redirect('lounge_inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'lounge/inventory/add.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lounge_inventory_list')
    else:
        form = CategoryForm()
    return render(request, 'lounge/inventory/add.html', {'form': form})

def inventory_list(request):
    items = Inventory.objects.all().order_by('-date')
    return render(request, 'lounge/inventory/list.html', {'items': items})


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
            return redirect('lounge_inventory_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = InventoryForm(instance=item)
    return render(request, 'lounge/inventory/update_inventory.html', {'form': form})


# Delete Inventory View
def delete_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        item.delete()
        # Respond to AJAX request with success message
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Inventory item deleted successfully!"})
        messages.success(request, "Inventory item deleted successfully!")
        return redirect('lounge_inventory_list')
    return render(request, 'lounge/inventory/delete_inventory.html', {'item': item})


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
    return render(request, 'lounge/sales_history.html', {
        'sales': sales_data,
        'graph_labels': graph_labels,
        'graph_values': graph_values,
    })

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import Sum

def sales_history(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
        # Handle AJAX request for sales data
        sales = Sale.objects.all().values('id', 'cashier__username', 'completed', 'total', 'paid' ,'date') # Query all sales data
        sales_list = list(sales)  # Convert queryset to list of dictionaries
        return JsonResponse({'sales': sales_list})

    # For non-AJAX requests, render the template
    return render(request, 'lounge/sales_history.html', { 
        'sales_data': Sale.objects.filter(completed=True).order_by('-date')[:10]  # Example: Latest 10 sales
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
from .models import Sale  # Assuming you have a Sale model for storing sales data
from datetime import datetime

def end_of_day_report(request):
    # Get today's date
    today = datetime.today().date()
    day = Day.objects.filter(staff=request.user).last()

    # Fetch the sales for today from the database
    sales = Sale.objects.filter(day=day)  # Assuming your Sale model has a 'date' field

    # Aggregate the sales data
    context = {
        'total_sales': sales.count(),
        'total_amount': sales.aggregate(total=Sum('total'))['total'] or 0,
        'sales': sales,
        'day': day,
    }

    return render(request, 'lounge/end-of-day.html', context)

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
        return redirect('lounge_start_day')  # Redirect to the start day view if no day has started
    
    unfinished_day.end_time  = datetime.now().time()
    unfinished_day.end = True
    unfinished_day.no_of_sales = Sale.objects.filter(day = unfinished_day).count()
    unfinished_day.end_amount = Sale.objects.filter(day = unfinished_day).aggregate(Sum('total'))['total__sum']
    unfinished_day.save()
    return redirect('lounge_end_of_day_report')  # Redirect to the start day view if no day has started

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
        "values": [item.quantity for item in inventory_data],
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
    return render(request, "lounge/audit_report.html", context)