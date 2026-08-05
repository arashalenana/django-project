from functools import wraps
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You do not have access to the dashboard.")
        return view_func(request, *args, **kwargs)
    return _wrapped

def dashboard_permission_required(perm):
    def decorator(view_func):
        @wraps(view_func)
        @staff_required
        @permission_required(perm, raise_exception=True)
        def _wrapped(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

def superuser_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("This action is restricted to superuser accounts.")
        return view_func(request, *args, **kwargs)
    return _wrapped