from .models import AppVariable

def app_variables(request):
    """
    Injects all AppVariable key-value pairs globally into template contexts.
    Access in templates via {{ app_vars.SITE_NAME }}, {{ app_vars.SUPPORT_EMAIL }}, etc.
    """
    try:
        vars_dict = {var.key: var.value for var in AppVariable.objects.all()}
    except Exception:
        vars_dict = {}
    return {'app_vars': vars_dict}