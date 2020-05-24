from django.contrib import admin

from companies.models import Company, WaitList


class CompanyAdmin(admin.ModelAdmin):

    model = Company

    fieldsets = (
        ('Contact Info', {
            'fields': (
                'name',
                'public_id',
                'website',
                'phone',
                'slug',

            )
        }
         ),
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
        }
         ),
        ('Brand', {
            'fields': (
                'logo',
                'logo_background_color',
                'cover_img',
            )
        }
         ),
        ('Admins', {
            'fields': (
                'admins',
            )
        }
         ),
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
admin.site.register(WaitList, WaitlistAdmin)
