from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboard_redirect_view


urlpatterns = [
    path('django-admin/', admin.site.urls),
    
    # Core CMS, AppVariables, and Public Landing
    path('', include('core.urls')),
    
    # Customer Accounts & Auth Dashboard
    path('accounts/', include('accounts.urls')),
    
    # Shipments, Tracking, & Customer Portal
    path('shipments/', include('shipments.urls')),
    
    # Support & Real-Time Chat Admin
    path('support/', include('support.urls')),
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
]
