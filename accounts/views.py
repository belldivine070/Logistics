from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages

from core.mixins import StaffRequiredMixin
from .models import CustomerProfile
from .forms import CustomerProfileForm, AdminCustomerCreationForm

User = get_user_model()


@login_required
def dashboard_redirect_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_shipment_list')
    return redirect('customer_portal')


class AdminCustomerListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class AdminCustomerCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = AdminCustomerCreationForm
    template_name = 'dashboard/customer_form.html'
    success_url = reverse_lazy('admin_customer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        role_type = "Admin/Staff" if self.object.is_staff else "Customer"
        messages.success(self.request, f"{role_type} account for {self.object.username} created successfully.")
        return response


class AdminCustomerUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = AdminCustomerCreationForm
    template_name = 'dashboard/customer_form.html'
    success_url = reverse_lazy('admin_customer_list')
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Customer account for {self.object.username} updated successfully.")
        return response


class AdminCustomerDeleteView(StaffRequiredMixin, View):
    """
    Handles immediate same-page deletion of a user via POST request.
    """
    def post(self, request, username, *args, **kwargs):
        user_to_delete = get_object_or_404(User, username=username)
        
        # Prevent deleting your own active superuser account accidentally
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete your own active account.")
            return redirect('admin_customer_list')

        username_str = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"Account '{username_str}' has been deleted successfully.")
        return redirect('admin_customer_list')


class CustomerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('customer_profile')

    def get_object(self, queryset=None):
        profile, created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)