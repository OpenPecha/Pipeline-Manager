from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def notify_monlamAI_tracker(payload):
    if payload["action"] != "closed":
        return

    issue = payload["issue"]
    repo = payload["repository"]

    if not issue["title"].startswith("EN") or not issue["title"].startswith("BO"):
        return

    if not issue["title"] == repo["name"]:
        return

    return Response({"success": True, "message": "Tracker notified"})


class GitHubWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        event_type = request.META.get("HTTP_X_GITHUB_EVENT")
        payload = request.data
        if event_type == "issues":
            notify_monlamAI_tracker(payload)
        else:
            return Response(
                {"success": False, "message": f"Invalid event type: {event_type}"}
            )
