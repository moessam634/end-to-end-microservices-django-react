from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware


class CsrfExemptApiMiddleware(MiddlewareMixin):
    """
    Middleware that exempts API routes from CSRF protection
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exempt API routes from CSRF
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        # For non-API routes, let Django's default CSRF middleware handle it
        # (which is already in MIDDLEWARE settings)
        return None
