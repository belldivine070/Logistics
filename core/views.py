from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.forms import modelformset_factory
from django import forms
from django.contrib import messages

from core.mixins import StaffRequiredMixin
from core.models import AppVariable


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass dynamic app variables into the template context
        context['app_vars'] = AppVariable.get_vars()
        return context


class AdminAppVariableUpdateView(StaffRequiredMixin, View):
    template_name = 'dashboard/app_variable_form.html'

    def get(self, request, *args, **kwargs):
        AppVarFormSet = modelformset_factory(
            AppVariable, 
            fields=('value', 'description'), 
            extra=0,
            widgets={
                'value': forms.TextInput(),
                'description': forms.TextInput(),
            }
        )
        formset = AppVarFormSet(queryset=AppVariable.objects.all().order_by('key'))
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        AppVarFormSet = modelformset_factory(
            AppVariable, 
            fields=('value', 'description'), 
            extra=0,
            widgets={
                'value': forms.TextInput(),
                'description': forms.TextInput(),
            }
        )
        formset = AppVarFormSet(request.POST, queryset=AppVariable.objects.all().order_by('key'))
        
        if formset.is_valid():
            formset.save()
            messages.success(request, "Global configuration variables updated successfully.")
            return redirect('admin_app_variables')
        
        return render(request, self.template_name, {'formset': formset})