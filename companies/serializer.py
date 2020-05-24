from rest_framework import serializers

from companies.models import Company


class BasicCompanySerializer(serializers.ModelSerializer):

    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'public_id',
            'name',
            'logo_url',
            'absolute_url'
        )


class CompanySerializer(serializers.ModelSerializer):
    from users.serializers import BasicCustomUserSerializer

    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    gmaps_url = serializers.URLField(source='get_gmaps_embed_url', read_only=True)
    admins = BasicCustomUserSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'public_id',
            'name',
            'slug',
            'absolute_url',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
            'website',
            'website_pretty',
            'phone_pretty',
            'gmaps_url',
            'logo_url',
            'admins'
        )
        depth = 1