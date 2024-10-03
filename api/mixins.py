from .models import PlatformApiCall
import json

class APILoggingMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        try:
            user = request.user if request.user.is_authenticated else None
            PlatformApiCall.objects.create(
                user=user,
                requested_url=request.build_absolute_uri(),
                requested_data=json.dumps(request.data) if request.data else '',
                response_data=response.content.decode('utf-8') if response.content else '',
            )
        except Exception as e:
            # Handle logging errors if necessary
            pass
        return response