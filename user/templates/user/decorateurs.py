from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.roles and request.user.roles.role_name == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Accès réservé aux administrateurs.")
    return wrapper