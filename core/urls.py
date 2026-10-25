from django.urls import path
from . import views


urlpatterns = [
    # Public Root & CMS Listings
    path('', views.HomeView.as_view(), name='home'),

    # Settings / AppVariables
    path('dashboard/settings/variables/', views.AdminAppVariableUpdateView.as_view(), name='admin_app_variables'),
]