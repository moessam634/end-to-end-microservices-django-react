from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt


class CsrfExemptApiMiddleware(MiddlewareMixin):
    """
    Middleware that exempts API routes from CSRF protection
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exempt API routes from CSRF
        if request.path.startswith('/api/'):
            # Set CSRF exempt flag
            setattr(request, '_dont_enforce_csrf_checks', True)
            return None
        
        # Use default CSRF middleware for other routes
        csrf_middleware = CsrfViewMiddleware()
        return csrf_middleware.process_view(request, view_func, view_args, view_kwargs)
