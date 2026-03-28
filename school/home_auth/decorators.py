from django.shortcuts import redirect, render
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views that checks whether a user has a particular role,
    redirecting to the login page if necessary, or rendering an access denied page.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
                
            # Superusers bypass the role check
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            has_permission = False
            
            if 'admin' in allowed_roles and getattr(request.user, 'is_admin', False):
                has_permission = True
            elif 'teacher' in allowed_roles and getattr(request.user, 'is_teacher', False):
                has_permission = True
            elif 'student' in allowed_roles and getattr(request.user, 'is_student', False):
                has_permission = True
                
            if has_permission:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'Home/access_denied.html', {'roles': allowed_roles})
                
        return _wrapped_view
    return decorator
