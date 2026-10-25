from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    AdminCustomerListView,
    AdminCustomerCreateView,
    AdminCustomerUpdateView,
    AdminCustomerDeleteView,
    CustomerProfileUpdateView,
)

urlpatterns = [
    # Auth Views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Customer Self-Management
    path('profile/', CustomerProfileUpdateView.as_view(), name='customer_profile'),

    # Staff Customer & Admin Management Dashboard
    path('dashboard/customers/', AdminCustomerListView.as_view(), name='admin_customer_list'),
    path('dashboard/customers/new/', AdminCustomerCreateView.as_view(), name='admin_customer_create'),
    path('dashboard/customers/<str:username>/edit/', AdminCustomerUpdateView.as_view(), name='admin_customer_update'),
    path('dashboard/customers/<str:username>/delete/', AdminCustomerDeleteView.as_view(), name='admin_customer_delete'),
]