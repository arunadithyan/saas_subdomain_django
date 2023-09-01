from django_tenants.middleware.main import TenantMainMiddleware
from django.http import HttpResponseForbidden

class TenantMiddleware(TenantMainMiddleware):
    """
    Field is_active can be used to temporary disable tenant and
    block access to their site. Modifying get_tenant method from
    TenantMiddleware allows us to check if tenant should be available
    """
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        if not tenant.is_active:
            raise self.TENANT_NOT_FOUND_EXCEPTION("Tenant is inactive")
        return tenant




from django.http import HttpResponseForbidden


class RestrictCreateTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # Check if the requested path is /create-tenant
        if request.path == '/create-tenant/':
            # Get the host from the request
            host = request.get_host()
            print(host)

            # Check if the request is from localhost
            if not host.startswith('localhost:'):
                return HttpResponseForbidden("Access Forbidden")

        return self.get_response(request)
