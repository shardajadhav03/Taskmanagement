from django.utils.deprecation import MiddlewareMixin
from .models import Visit

class UniqueVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Check if the IP address is already in the Visit model
        if not Visit.objects.filter(ip_address=ip_address).exists():
            Visit.objects.create(ip_address=ip_address)