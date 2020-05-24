from django.contrib import admin

from companies.models import Company, WaitList


class CompanyAdmin(admin.ModelAdmin):

    class Meta:
        model = Company


class WaitlistAdmin(admin.ModelAdmin):

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)
admin.site.register(WaitList, WaitlistAdmin)
