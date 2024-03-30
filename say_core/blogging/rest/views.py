from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from say_core.blogging.rest.serializers import WPSiteRegisterAPIKeySerializer


class WPSiteAPIKeyViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = WPSiteRegisterAPIKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wp_register_obj, apikey = serializer.save()
        return Response({"apikey": apikey}, status=status.HTTP_201_CREATED)
