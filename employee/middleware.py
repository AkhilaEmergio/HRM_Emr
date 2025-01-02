from django.utils.deprecation import MiddlewareMixin
from employee.models import Organization

class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.get_host().split(':')[0]  # Extract domain (e.g., orgname.hrstop.com)
        try:
            organization = Organization.objects.get(domain=domain)
            request.organization = organization
        except Organization.DoesNotExist:
            request.organization = None
