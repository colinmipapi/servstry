from django.contrib import admin

from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone'
        )


admin.site.register(CustomUser, CustomUserAdmin)
