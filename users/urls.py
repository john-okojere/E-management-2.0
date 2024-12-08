from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='customusers'),
    path('add/', views.add_user, name='add_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboards'),
    path('face-auth', views.face_auth, name='face-auth'),
    path('choose_section/', views.choose_section, name='choose_section'),
]
