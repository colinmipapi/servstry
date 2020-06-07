from django.contrib import admin

from track.models import (
    GuestVisit,
    CustomSafetyPolicy
)

from rangefilter.filter import DateRangeFilter


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
        ('arrival', DateRangeFilter),
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


class CustomSafetyPolicyAdmin(admin.ModelAdmin):

    model = CustomSafetyPolicy

    fields = (
        'public_id',
        'created',
        'company',
        'policy_text'
    )
    list_display = (
        'company',
        'created',
        'public_id'
    )
    search_fields = (
        'company',
    )
    readonly_fields = (
        'public_id',
        'created',
        'company',
    )


admin.site.register(GuestVisit, GuestVisitAdmin)
admin.site.register(CustomSafetyPolicy, CustomSafetyPolicyAdmin)
