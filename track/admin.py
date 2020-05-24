from django.contrib import admin

from track.models import GuestVisit


class GuestVisitAdmin(admin.ModelAdmin):
    model = GuestVisit

    fieldsets = (
        ('Guest Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone'
            )
        }),
        ('Visit Information', {
            'fields': (
                'confirmation',
                'company',
                'arrival',
                'departure'
            )
        }),
        ('Internal Information', {
            'fields': (
                'public_id',
                'submitted',
                'ip_address'
            )
        })
    )
    list_display = (
        'last_name',
        'first_name',
        'arrival',
        'company',
        'confirmation'
    )
    list_filter = (
        'company',
    )
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'company',
        'confirmation'
    )
    readonly_fields = (
        'public_id',
        'submitted',
        'ip_address',
        'confirmation'
    )


admin.site.register(GuestVisit, GuestVisitAdmin)