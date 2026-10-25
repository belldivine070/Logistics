from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    default_shipping_address = models.ForeignKey(
        'shipments.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_shipping_profiles'
    )

    def __str__(self):
        return f"Profile for {self.user.email or self.user.username}"


# Signal: Automatically create a CustomerProfile when a new User is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)
    else:
        # Ensures existing profiles don't throw AttributeError on save
        if hasattr(instance, 'profile'):
            instance.profile.save()