import os
import django
from django.conf import settings
from django.http import JsonResponse

# This is for debugging Vercel deployment
def handler(request):
    try:
        # Import your models to test DB connection
        from home.models import CustomUser
        
        # Test database connection
        user_count = CustomUser.objects.count()
        
        return JsonResponse({
            'status': 'OK',
            'debug': True,
            'database_url_set': bool(os.getenv('DATABASE_URL')),
            'secret_key_set': bool(os.getenv('SECRET_KEY')),
            'allowed_hosts': os.getenv('ALLOWED_HOSTS', 'Not set'),
            'user_count': user_count,
            'django_version': django.get_version()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'ERROR',
            'error': str(e),
            'database_url_set': bool(os.getenv('DATABASE_URL')),
            'secret_key_set': bool(os.getenv('SECRET_KEY')),
        }, status=500)