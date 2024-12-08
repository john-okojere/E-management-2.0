from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('face-authentication/', TemplateView.as_view(template_name='face-authentication.html'), name='face-authentication'),
]