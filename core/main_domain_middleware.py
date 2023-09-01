# main_domain_middleware.py
# from django.conf import settings

# class MainDomainMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Get the host from the request
#         request_host = request.get_host()

#         # Print the host for debugging
#         print(f"Request Host: {request_host}")

#         # Check if the request's host is 'localhost:8000'
#         if request_host == 'localhost:8000':
#             settings.REGISTER_MODEL_FOR_MAIN_DOMAIN = True
#         else:
#             settings.REGISTER_MODEL_FOR_MAIN_DOMAIN = False

#         # Print the value of REGISTER_MODEL_FOR_MAIN_DOMAIN for debugging
#         print(f"REGISTER_MODEL_FOR_MAIN_DOMAIN: {settings.REGISTER_MODEL_FOR_MAIN_DOMAIN}")

#         response = self.get_response(request)
#         return response

# myapp/middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

class RegisterModelMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/tenant/tenant/':
            # Get the host from the request
            host = request.get_host()
            print(host)
            if not host.startswith('localhost:'):
                return HttpResponseForbidden("Access Forbidden")
        return self.get_response(request)

    # def process_request(self, request):
    #     host = request.META.get('HTTP_HOST')
    #     print(host)
    #     if host == 'localhost:8000' :
    #         settings.REGISTER_MODEL_FOR_MAIN_DOMAIN = True
    #     else:
    #         settings.REGISTER_MODEL_FOR_MAIN_DOMAIN = False

