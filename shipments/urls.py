from django.urls import path
from .views import (
    PublicTrackingView,
    CustomerPortalDashboardView,
    CustomerShipmentDetailView,
    AdminShipmentListView,
    AdminShipmentCreateView,
    AdminShipmentUpdateView,
)

urlpatterns = [
    # Public Unauthenticated Tracking Page
    path('track/<str:tracking_number>/', PublicTrackingView.as_view(), name='public_tracking'),

    # Logged-in Customer Isolated Portal
    path('portal/', CustomerPortalDashboardView.as_view(), name='customer_portal'),
    path('portal/<str:tracking_number>/', CustomerShipmentDetailView.as_view(), name='customer_shipment_detail'),

    # Staff Operations Dashboard
    path('dashboard/manage/', AdminShipmentListView.as_view(), name='admin_shipment_list'),
    path('dashboard/manage/new/', AdminShipmentCreateView.as_view(), name='admin_shipment_create'),
    path('dashboard/manage/<str:tracking_number>/edit/', AdminShipmentUpdateView.as_view(), name='admin_shipment_update'),
]


from django.urls import path
from .views import (
    AdminShipmentListView,
    AdminShipmentCreateView,
    AdminShipmentUpdateView,
    AdminLocationListView,
    AdminLocationCreateView,
    AdminLocationUpdateView,
    AdminLocationDeleteView,
    PublicTrackingView,
    CustomerPortalDashboardView,
    CustomerShipmentDetailView,
)

urlpatterns = [
    # Shipment Admin Management Routes
    path('dashboard/shipments/', AdminShipmentListView.as_view(), name='admin_shipment_list'),
    path('dashboard/shipments/new/', AdminShipmentCreateView.as_view(), name='admin_shipment_create'),
    # path('dashboard/shipments/<int:pk>/edit/', AdminShipmentUpdateView.as_view(), name='admin_shipment_update'),
    path('dashboard/shipments/<str:tracking_number>/edit/', AdminShipmentUpdateView.as_view(), name='admin_shipment_update'),

    # Location Management Routes (CRUD)
    path('dashboard/locations/', AdminLocationListView.as_view(), name='admin_location_list'),
    path('dashboard/locations/new/', AdminLocationCreateView.as_view(), name='admin_location_create'),
    path('dashboard/locations/<int:pk>/edit/', AdminLocationUpdateView.as_view(), name='admin_location_update'),
    path('dashboard/locations/<int:pk>/delete/', AdminLocationDeleteView.as_view(), name='admin_location_delete'),

    # Public & Customer Tracking Routes
    path('track/<str:tracking_number>/', PublicTrackingView.as_view(), name='public_tracking'),
    path('portal/shipments/', CustomerPortalDashboardView.as_view(), name='customer_portal'),
    path('portal/shipments/<str:tracking_number>/', CustomerShipmentDetailView.as_view(), name='customer_shipment_detail'),
]