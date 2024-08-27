from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse

from toggles.models import Toggle


# Create your views here.


def update_toggle(request: HttpRequest, toggle_id: int) -> HttpResponse:
    if request.method == "PUT":
        try:
            toggle = Toggle.objects.get(id=toggle_id)
            toggle.enabled = not toggle.enabled
            toggle.save()
            return JsonResponse({}, status=204)
        except Toggle.DoesNotExist:
            return JsonResponse({"message": "Toggle not found"}, status=404)
    return JsonResponse({"message": "Method not allowed"}, status=405)
