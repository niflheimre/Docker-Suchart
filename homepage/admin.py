from django.contrib import admin

# Register your models here.
from .models import case


def approve(modeladmin, request, queryset):
    queryset.update(status='1')
approve.short_description = 'Mark selected case as approved'

def reject(modeladmin, request, queryset):
    queryset.update(status='0')
reject.short_description = 'Mark selected case as not approved'

class caseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in case._meta.get_fields()]
    search_fields = ("name", "goods", "bank_num", "nat_id","website")
    list_filter = ('report_date','status')
    actions = [approve,reject]

admin.site.register(case,caseAdmin)


