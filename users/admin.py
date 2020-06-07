from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Invitation

# Admin Site Settings

admin.site.site_header = "Servstry"
admin.site.site_title = "Servstry"
admin.site.index_title = "Servstry"


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
