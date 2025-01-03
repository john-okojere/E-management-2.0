from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

