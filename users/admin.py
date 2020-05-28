from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Invitation


class CustomUserAdmin(UserAdmin):

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone'
        )


class InvitationAdmin(admin.ModelAdmin):
    model = Invitation


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Invitation, InvitationAdmin)
