from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Invitation


class CustomUserAdmin(UserAdmin):

    model = CustomUser
    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'id',
                'public_id'
            )
        }
         ),
    )
    list_display = (
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'last_login'
    )
    readonly_fields = (
        'id',
        'public_id',
    )


class InvitationAdmin(admin.ModelAdmin):
    model = Invitation


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Invitation, InvitationAdmin)
