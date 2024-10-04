from rest_framework import status
from rest_framework.response import Response
from functools import wraps

def customer_only(view_func):
    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):
        if hasattr(request.user, 'customer'):
            return view_func(view, request, *args, **kwargs)
        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    return _wrapped_view