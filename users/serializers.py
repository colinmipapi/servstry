from rest_framework import serializers

from users.models import (
    CustomUser,
)


class BasicCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'username'
        )


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'public_id',
            'first_name',
            'last_name',
            'phone',
            'email'
        )
