from django.contrib import admin

from companies.models import Company
from track.models import CustomSafetyPolicy


class AdminsInline(admin.TabularInline):
    model = Company.admins.through
    extra = 0


class CustomSafetyPolicyInline(admin.TabularInline):
    model = CustomSafetyPolicy
    extra = 0


class CompanyAdmin(admin.ModelAdmin):

    model = Company

    fieldsets = (
        ('Contact Info', {
            'fields': (
                'name',
                'status',
                'public_id',
                'website',
                'phone',
                'slug',

            )
        }),
        ('Location', {
            'fields': (
                'address1',
                'address2',
                'city',
                'state',
                'zip_code',
                'lat',
                'lng',
                'place_id',
            )
        }),
        ('Brand', {
            'fields': (
                'logo',
                'logo_background_color',
                'cover_img',
            )
        }),
        ('Stripe', {
            'fields': (
                'customer_id',
            )
        }),
    )
    list_display = (
        'name',
        'city',
        'state',
    )
    search_fields = (
        'name',
        'city',
        'state'
    )
    readonly_fields = (
        'public_id',
    )
    inlines = (
        AdminsInline,
        CustomSafetyPolicyInline
    )


class WaitlistAdmin(admin.ModelAdmin):

    model = Company

    fields = (
        'public_id',
        'submitted',
        'email'
    )
    list_display = (
        'email',
        'submitted'
    )
    search_fields = (
        'email',
    )
    readonly_fields = (
        'public_id',
        'submitted'
    )


admin.site.register(Company, CompanyAdmin)
