from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from say_core.blogging.rest.serializers import WPSiteRegisterAPIKeySerializer


class WPSiteAPIKeyViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = WPSiteRegisterAPIKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wp_register_obj = serializer.save()
        return Response(WPSiteRegisterAPIKeySerializer(instance=wp_register_obj))
