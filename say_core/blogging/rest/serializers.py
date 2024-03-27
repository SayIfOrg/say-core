from urllib.parse import urljoin

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as __, gettext as _
from rest_framework import serializers, status
from rest_framework_api_key.models import APIKey

from say_core.blogging.models import WPSiteModel, WPRegisterModel


class WPSiteRegisterAPIKeySerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_initiation_code": "{message}",
        "unsuccessful_ping": __("ping to {ping_url} was unsuccessful, detail: {detail}"),
    }
    initiation_code = serializers.CharField(write_only=True)
    site_url = serializers.URLField(write_only=True)
    apikey = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # validate initiation_code
        wp_register_obj = WPRegisterModel.objects.filter(code=attrs["initiation_code"]).order_by("-code_generated_at").first()
        if wp_register_obj is None:
            self.fail("invalid_initiation_code", message=_("this code is invalid."))
        if wp_register_obj.code_used_at is not None:
            self.fail("invalid_initiation_code", message=_("this code is already used."))
        if (timezone.now() - wp_register_obj.code_generated_at) > settings.WP_GENERATED_CODE_VALID_TIME:
            self.fail("invalid_initiation_code", message=_("this code is expired."))
        attrs["wp_register_obj"] = wp_register_obj

        # pinging
        site_url = attrs["site_url"]
        ping_url = urljoin(site_url, settings.WP_PLUGIN["ping_url"])
        try:
            r = requests.post(ping_url, json={"initiation_code": attrs["initiation_code"]})
            if r.status_code != status.HTTP_200_OK:
                self.fail("unsuccessful_ping", ping_url=ping_url, detail=r.text)
        except requests.exceptions.ConnectionError as e:
            self.fail("unsuccessful_ping", ping_url=ping_url, detail=str(e))
        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        wp_site_obj = WPSiteModel()
        wp_site_obj.url = validated_data["site_url"]
        wp_site_obj.save()
        apikey = APIKey.objects.create_key(name="wp plugin")
        wp_register_obj = validated_data["wp_register_obj"]
        wp_register_obj.site = wp_register_obj
        wp_register_obj.code_used_at = timezone.now()
        wp_register_obj.status = wp_register_obj.Status.REGISTERED
        wp_register_obj.apikey = apikey
        wp_register_obj.save()
        return wp_register_obj


