import random
import string
from django.db import models
from django.conf import settings
from .services import geocode_address


class Location(models.Model):
    name = models.CharField(max_length=255, help_text="e.g. Chicago Distribution Center")
    address = models.TextField(blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=150, default="United States")

    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            full_query = f"{self.name}, {self.address}, {self.city}, {self.state} {self.postal_code}, {self.country}"
            coords = geocode_address(full_query)
            if coords:
                self.latitude, self.longitude = coords
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Shipment Created'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('EXCEPTION', 'Exception / Delayed'),
    ]

    SERVICE_CHOICES = [
        ('STANDARD_GROUND', 'Standard Ground Shipping'),
        ('EXPRESS_AIR', 'Express Air Freight'),
        ('OVERNIGHT_PRIORITY', 'Overnight Priority'),
        ('OCEAN_FREIGHT', 'International Ocean Freight'),
        ('HEAVY_CARGO', 'Heavy Cargo Transport'),
    ]

    tracking_number = models.CharField(max_length=50, unique=True, blank=True, db_index=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    
    origin = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='shipments_origin')
    destination = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='shipments_destination')
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments_current')
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='CREATED')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='STANDARD_GROUND')
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate custom uppercase tracking number if missing
        if not self.tracking_number:
            prefix = "USL"
            while True:
                suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                code = f"{prefix}-{suffix}"
                if not Shipment.objects.filter(tracking_number=code).exists():
                    self.tracking_number = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"


class TrackingEvent(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.shipment.tracking_number} @ {self.timestamp}: {self.status}"