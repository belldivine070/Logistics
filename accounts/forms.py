from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerProfile

User = get_user_model()


class AdminCustomerCreationForm(forms.ModelForm):
    """
    Form for staff/administrators to register a new customer or admin account manually.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 text-sm'}),
        required=True,
        help_text="Enter a secure password for the user."
    )
    is_staff = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        help_text="Designates whether the user can log into this admin site."
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        help_text="Designates whether this user should be treated as active."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply clean Tailwind styling to standard inputs
        for field_name, field in self.fields.items():
            if field_name not in ['is_staff', 'is_active'] and 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class CustomerProfileForm(forms.ModelForm):
    """
    Form for customers to update their personal profile info (phone, company).
    """
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 text-sm'}))
    company_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 text-sm'}))

    class Meta:
        model = CustomerProfile
        fields = ('phone_number', 'company_name', 'default_shipping_address')
        widgets = {
            'default_shipping_address': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 text-sm'}),
        }