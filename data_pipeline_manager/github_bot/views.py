from rest_framework.response import Response
from rest_framework.views import APIView


class GitHubWebhookView(APIView):
    def post(self, request):
        event_type = request.META.get("HTTP_X_GITHUB_EVENT")
        payload = request.data
        if event_type == "push":
            print(payload)
            return Response({"success": True})
        else:
            return Response(
                {"success": False, "message": f"Invalid event type: {event_type}"}
            )
