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
