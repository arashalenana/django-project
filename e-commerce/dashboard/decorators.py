from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def staff_required(view_func):
    
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You do not have access to the dashboard.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped


def dashboard_permission_required(perm):
   
    def decorator(view_func):
        @wraps(view_func)
        @staff_required
        def _wrapped(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                messages.error(request, "You do not have permission to access that section.")
                return redirect('dashboard:home')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def superuser_required(view_func):

    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "This action is restricted to superuser accounts.")
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return _wrapped