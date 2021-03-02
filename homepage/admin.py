from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

# Register your models here.
from .models import case,Tweet


def verify(modeladmin, request, queryset):
    queryset.update(status='1')
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(
            user_id = request.user.id,
            content_type_id = ct.pk,
            object_id = obj.pk,
            object_repr = 'Verified :'+str(obj),
            action_flag = CHANGE,
            change_message = 'Mark as Verified.')
verify.short_description = 'Mark selected case as Verified.'

def reject(modeladmin, request, queryset):
    queryset.update(status='0')
    ct = ContentType.objects.get_for_model(queryset.model)
    for obj in queryset:
        LogEntry.objects.log_action(
            user_id = request.user.id,
            content_type_id = ct.pk,
            object_id = obj.pk,
            object_repr = 'Unverified :'+str(obj),
            action_flag = CHANGE,
            change_message = 'Mark as not Unverified.')
reject.short_description = 'Mark selected case as Unverified.'

def trainmod(modeladmin, request, queryset):
    print('In progress')
trainmod.short_description = 'Train model with selected data.'

class caseAdmin(admin.ModelAdmin):
    
    def isVerified(self,instance):
        return instance.status == '1'

    isVerified.boolean = True
    isVerified.short_description = 'Verified'
    isVerified.admin_order_field = 'status'

    list_display = ['isVerified','id','name','goods','price','nat_id','bank_num']
    list_display_links = ('name',)

    search_fields = ("name", "goods", "bank_num", "nat_id","website")
    list_filter = ('report_date','status')
    actions = [verify,reject]
    ordering = ['status']

class tweetAdmin(admin.ModelAdmin):
    
    def isTrained(self,instance):
        return instance.status == '1'

    isTrained.boolean = True
    isTrained.short_description = 'Trained'
    isTrained.admin_order_field = 'status'

    list_display = ['isTrained','user','post']
    list_display_links = ('user',)

    search_fields = ('user','post')
    list_filter = ('status',)
    actions = [trainmod]
    ordering = ['status']


admin.site.register(case, caseAdmin)
admin.site.register(Tweet,tweetAdmin)
admin.site.site_title = 'Suchart'
admin.site.site_header = 'Suchart Administration'

