from .models import PlatformApiCall
from django.utils import timezone

class PlatformApiCallMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        # Log the API call only if the user is authenticated
        if request.user.is_authenticated:
            PlatformApiCall.objects.create(
                user=request.user,
                requested_url=request.build_absolute_uri(),
                requested_data=request.data if request.method in ['POST', 'PUT', 'PATCH'] else {},
                response_data=response.data,
                timestamp=timezone.now()
            )
        return super().finalize_response(request, response, *args, **kwargs)