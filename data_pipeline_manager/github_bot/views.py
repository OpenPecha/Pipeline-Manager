from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def notify_monlamAI_tracker(payload):
    if payload["action"] != "closed":
        print("not closed issue")
        return

    issue = payload["issue"]
    repo = payload["repository"]

    if not issue["title"].startswith("EN") and not issue["title"].startswith("BO"):
        print("not EN or BO issue", issue["title"])
        return

    if not issue["title"] == repo["name"]:
        print("not same repo name", issue["title"], repo["name"])
        return

    return True


class GitHubWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        event_type = request.META.get("HTTP_X_GITHUB_EVENT")
        payload = request.data
        if event_type == "issues":
            created = notify_monlamAI_tracker(payload)
            if created:
                return Response({"success": True})
            else:
                return Response(
                    {
                        "success": False,
                        "message": f"Invalid issue action: {payload['action']}",
                    }
                )
        else:
            return Response(
                {"success": False, "message": f"Invalid event type: {event_type}"}
            )
