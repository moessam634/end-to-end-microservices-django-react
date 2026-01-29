from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for monitoring and load balancers
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['checks']['database'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
    
    # Check Redis connection (if configured)
    try:
        cache.get('health_check')
        health_status['checks']['cache'] = 'healthy'
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        health_status['checks']['cache'] = 'unhealthy'
        # Don't mark overall status as unhealthy for cache issues
    
    # Check if we can write to cache
    try:
        cache.set('health_check', 'ok', 10)
        health_status['checks']['cache_write'] = 'healthy'
    except Exception as e:
        logger.warning(f"Cache write health check failed: {e}")
        health_status['checks']['cache_write'] = 'unhealthy'
    
    # Return appropriate HTTP status code
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JsonResponse(health_status, status=status_code)

def readiness_check(request):
    """
    Readiness check endpoint for Kubernetes readiness probes
    """
    readiness_status = {
        'status': 'ready',
        'checks': {}
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        readiness_status['checks']['database'] = 'ready'
    except Exception as e:
        logger.error(f"Database readiness check failed: {e}")
        readiness_status['checks']['database'] = 'not_ready'
        readiness_status['status'] = 'not_ready'
    
    # Return appropriate HTTP status code
    status_code = 200 if readiness_status['status'] == 'ready' else 503
    
    return JsonResponse(readiness_status, status=status_code)

def liveness_check(request):
    """
    Liveness check endpoint for Kubernetes liveness probes
    """
    return JsonResponse({'status': 'alive'}, status=200)
