from time import time
from api.getMeetSession import generateMeetUrl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)  # Import IsAuthenticated permission class


class MySecureAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Apply IsAuthenticated permission to this view

    def get(self, request):
        # Your API logic for GET request
        data = {"status": 403, "response": {"Access Forbidden. Method GET not allowed"}}
        return Response(data=data, status=403)

    def post(self, request):
        # Your API logic for POST request
        meet_url = generateMeetUrl()
        data = {
            "status": 200,
            "response": {
                "meet_url": f"{meet_url}",
                "timestamp": str(time()).split(".")[0],
            },
        }

        return Response(data, status=200)
