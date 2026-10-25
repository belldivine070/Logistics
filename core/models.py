from django.db import models
from django.core.cache import cache


class AppVariable(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.key} = {self.value}"

    @classmethod
    def get_vars(cls):
        """
        Retrieves all application configuration variables as a dictionary,
        leveraging Django's cache for performance.
        """
        vars_dict = cache.get('app_variables')
        if vars_dict is None:
            vars_dict = {var.key: var.value for var in cls.objects.all()}
            cache.set('app_variables', vars_dict, timeout=None)
        return vars_dict

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache whenever a variable is modified in admin
        cache.delete('app_variables')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('app_variables')


        