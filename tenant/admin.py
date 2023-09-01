# from django.contrib import admin
# from django_tenants.admin import TenantAdminMixin
# from .models import Domain, Tenant
# from django.conf import settings

# class DomainInline(admin.TabularInline):
#     model = Domain
#     max_num = 1


# # admin.site.register(Tenant)

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Tenant
from django.conf import settings

class CustomTenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = (
        "user",
        "is_active",
        "created_on",
    )

    def has_add_permission(self, request):
        # Check if the request's host is 'localhost:8000'
        if request.get_host() == 'localhost:8000':
            return True
        return False

# Register the custom admin view for Tenant model

admin.site.register(Tenant, CustomTenantAdmin)
