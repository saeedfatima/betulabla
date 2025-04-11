from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test

def coordinator_required(view_func):
    """
    Allows access only to users who have an associated staffprofile with the role 'coordinator'.
    If no profile is found or the role does not match, returns HTTP 403 Forbidden.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Try to access the staffprofile; if not present, forbid access.
        try:
            profile = request.user.staffprofile
        except AttributeError:
            return HttpResponseForbidden("Coordinator profile not found.")
        
        # Check that the role is 'coordinator' (case-insensitive).
        if str(profile.role).lower() == 'coordinator':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return _wrapped_view


def group_required(group_name, login_url='login', raise_exception=False):
    """
    Decorator for views that checks whether a user is in a specific group, redirecting to the
    login page if necessary. If `raise_exception` is True, a PermissionDenied exception is raised
    instead of redirecting.
    
    Usage:
        @group_required('Coordinator')
        def my_view(request):
            ...
    """
    def in_group(user):
        is_in_group = user.is_authenticated and user.groups.filter(name=group_name).exists()
        if not is_in_group and raise_exception:
            raise PermissionDenied
        return is_in_group

    return user_passes_test(in_group, login_url=login_url)
