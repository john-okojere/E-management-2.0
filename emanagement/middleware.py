from django.shortcuts import redirect
from django.urls import reverse, resolve

SECTIONS = [
    'restaurant',
    'arcade',
    'cosmetic_store',
    'salon',
    'fashion',
    'spa',
    'lounge',
]

class RoleBasedRedirectMiddleware:
    """
    Middleware to handle redirection for authenticated users based on their roles and sections.
    Includes face authentication enforcement and skips staff users.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for unauthenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip middleware for staff users
        if request.user.is_staff:
            return self.get_response(request)

        # Exclude static and media paths
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Define exempt URLs (accessible to all authenticated users)
        exempt_urls = [
            reverse('face-auth'),  # Face authentication page
            reverse('logout'),     # Logout page
            '/digi02/',
        ]
        if request.path in exempt_urls:
            return self.get_response(request)

        # Ensure face authentication is completed
        if not request.session.get('face_authenticated', False):
            return redirect('face-auth')

        # Role and section-based redirection logic
        user_role = getattr(request.user, 'role', None)
        user_section = getattr(request.user, 'section', None)

        # Allowed paths based on user roles
        allowed_paths = []

        if user_role == 'Cashier' and user_section and user_section.lower() in SECTIONS:
            allowed_paths.extend([
                f'/{user_section.lower()}/cashier/',
                f'/{user_section.lower()}/sales-history/',
                f'/{user_section.lower()}/end-of-day-report/',
                f'/{user_section.lower()}/start_day/',
                f'/{user_section.lower()}/add-sale-item/',
                f'/{user_section.lower()}/create-sale/',
                f'/{user_section.lower()}/Pay-for-sale/',
                f'/{user_section.lower()}/make-payment/',
                f'/{user_section.lower()}/end_day/',
                f'/{user_section.lower()}/complete-sale/',
                f'/{user_section.lower()}/process-payment/',
                f'/{user_section.lower()}/approve-order/',
                f'/{user_section.lower()}/api/inventory/',
                f'/{user_section.lower()}/quantity-increase/<int:sale_item_id>/',
                f'/{user_section.lower()}/quantity-increase/<int:sale_item_id>/',
                f'/{user_section.lower()}/update-sale-item/<int:sale_item_id>/',
                f'/{user_section.lower()}/remove-sale-item/<int:sale_item_id>/',
                f'/{user_section.lower()}/get-order-details/<int:sale_id>/',
                f'/{user_section.lower()}/get-receipt-details/<int:sale_id>/',
                

            ])
        elif user_role == 'Manager' and user_section and user_section.lower() in SECTIONS:
            allowed_paths.extend([
                f'/{user_section.lower()}/dashboard/',
                f'/{user_section.lower()}/sales-history/',
                f'/{user_section.lower()}/reports/',
                f'/{user_section.lower()}/inventory/',
                f'/{user_section.lower()}/upload-inventory/',
                f'/{user_section.lower()}/api/sales-growth/',
                f'/{user_section.lower()}/api/sales-performance',
                f'/{user_section.lower()}/manage-approvals/',
                f'/{user_section.lower()}/api/inventory/',
                f'/{user_section.lower()}/export/pdf/',
                f'/{user_section.lower()}/export/excel/',
                f'/{user_section.lower()}/export/doc/',
                f'/{user_section.lower()}/approve-day/<int:day_id>/',
            ])
        elif user_role == 'Waiter' and user_section and user_section.lower() in SECTIONS:
            allowed_paths.extend([
                f'/{user_section.lower()}/waiter/',
                f'/{user_section.lower()}/send-cashier/',
                f'/{user_section.lower()}/create-sale/',
                f'/{user_section.lower()}/increase-sale-item/',
                f'/{user_section.lower()}/decrease-sale-item/',
                f'/{user_section.lower()}/add-sale-item/',
                f'/{user_section.lower()}/delete-sale-item/',
                f'/{user_section.lower()}/complete-sale/',
                f'/{user_section.lower()}/set-sale-type/',
                f'/{user_section.lower()}/update-table-number/',
            ])

        # Include dynamic URL patterns
        allowed_paths.append(f'/{user_section.lower()}/sale/receipt/<int:sale_id>/')

        path = request.path
        print(user_role,user_section,request.path,'Denied access')
        # Store last valid path in session if it's allowed
        if path in allowed_paths or any(path.startswith(ap.rstrip('<int:sale_id>/')) for ap in allowed_paths):
            request.session[f'last_valid_url_{user_role.lower()}'] = path
        elif path in allowed_paths or any(path.startswith(ap.rstrip('<int:day_id>/')) for ap in allowed_paths):
            request.session[f'last_valid_url_{user_role.lower()}'] = path
        elif path in allowed_paths or any(path.startswith(ap.rstrip('<int:sale_item_id>/')) for ap in allowed_paths):
            request.session[f'last_valid_url_{user_role.lower()}'] = path
        else:
            # Default redirects if no valid URL in session
            if user_role == 'Cashier' and user_section:
                return redirect(f'/{user_section.lower()}/cashier/')
            elif user_role == 'Manager' and user_section:
                return redirect(f'/{user_section.lower()}/dashboard/')
            elif user_role == 'Manager' and user_section:
                return redirect(f'/{user_section.lower()}/waiter/')

        return self.get_response(request)
    


