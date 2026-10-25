from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Shipment, Location
from core.mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404


class AdminShipmentListView(StaffRequiredMixin, ListView):
    model = Shipment
    template_name = 'dashboard/shipment_list.html'
    context_object_name = 'shipments'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related('origin', 'destination', 'current_location', 'customer')
        status_filter = self.request.GET.get('status')
        query = self.request.GET.get('q')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if query:
            queryset = queryset.filter(tracking_number__icontains=query)
        return queryset


class AdminShipmentCreateView(StaffRequiredMixin, CreateView):
    model = Shipment
    # tracking_number removed from fields so it auto-generates
    fields = ['customer', 'origin', 'destination', 'current_location', 'service_type', 'estimated_delivery', 'status']
    template_name = 'dashboard/shipment_form.html'
    success_url = reverse_lazy('admin_shipment_list')

    def form_valid(self, form):
        # Default current_location to origin if not explicitly provided
        if not form.cleaned_data.get('current_location'):
            form.instance.current_location = form.cleaned_data.get('origin')
        messages.success(self.request, "Shipment created successfully with an auto-generated tracking number.")
        return super().form_valid(form)


class AdminShipmentUpdateView(StaffRequiredMixin, UpdateView):
    model = Shipment
    fields = ['status', 'current_location', 'service_type', 'estimated_delivery']
    template_name = 'dashboard/shipment_form.html'
    slug_field = 'tracking_number'
    slug_url_kwarg = 'tracking_number'
    success_url = reverse_lazy('admin_shipment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all().order_by('name')
        return context

    def form_valid(self, form):
        messages.success(self.request, "Shipment updated successfully.")
        return super().form_valid(form)


class PublicTrackingView(DetailView):
    """
    Public unauthenticated tracking view for customers and visitors
    to look up real-time shipment status and location via tracking number.
    """
    model = Shipment
    template_name = 'shipments/public_tracking.html'
    context_object_name = 'shipment'
    slug_field = 'tracking_number'
    slug_url_kwarg = 'tracking_number'

    def get_queryset(self):
        return Shipment.objects.select_related('origin', 'destination', 'current_location').prefetch_related('events__location')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            messages.error(self.request, "The tracking number provided is invalid or does not exist.")
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('home')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CustomerPortalDashboardView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = 'dashboard/customer_portal.html'
    context_object_name = 'shipments'
    paginate_by = 10

    def get_queryset(self):
        # Strict security isolation: Only fetch shipments owned by request.user
        return Shipment.objects.filter(customer=self.request.user).select_related(
            'origin', 'destination', 'current_location'
        ).order_by('-created_at')


class CustomerShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = 'dashboard/shipment_detail.html'
    context_object_name = 'shipment'
    slug_field = 'tracking_number'
    slug_url_kwarg = 'tracking_number'

    def get_queryset(self):
        # Strict security isolation: Prevents accessing another user's tracking detail URL
        return Shipment.objects.filter(customer=self.request.user)


class AdminLocationListView(StaffRequiredMixin, ListView):
    model = Location
    template_name = 'dashboard/location_list.html'
    context_object_name = 'locations'
    paginate_by = 25

    def get_queryset(self):
        return Location.objects.all().order_by('-created_at')


class AdminLocationCreateView(StaffRequiredMixin, CreateView):
    model = Location
    fields = ['name', 'address', 'city', 'state', 'postal_code', 'country']
    template_name = 'dashboard/location_form.html'
    success_url = reverse_lazy('admin_location_list')

    def form_valid(self, form):
        messages.success(self.request, "Location created successfully. Coordinates geocoded.")
        return super().form_valid(form)


class AdminLocationUpdateView(StaffRequiredMixin, UpdateView):
    model = Location
    fields = ['name', 'address', 'city', 'state', 'postal_code', 'country']
    template_name = 'dashboard/location_form.html'
    success_url = reverse_lazy('admin_location_list')

    def form_valid(self, form):
        messages.success(self.request, "Location updated successfully.")
        return super().form_valid(form)


class AdminLocationDeleteView(StaffRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('admin_location_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Location deleted successfully.")
        return super().delete(request, *args, **kwargs)