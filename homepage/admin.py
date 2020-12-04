from django.contrib import admin

# Register your models here.
from .models import case


class caseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in case._meta.get_fields()]
    search_fields = ("name", "goods", "bank_num", "nat_id","website")
    list_filter = ('report_date',)
admin.site.register(case,caseAdmin)


