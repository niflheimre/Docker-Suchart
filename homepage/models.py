from django.db import models

# Create your models here.
class case(models.Model):
    name = models.CharField(max_length=60)
    nat_id = models.CharField(max_length=14, null=True, blank=True)
    goods = models.CharField(max_length=40)
    price = models.FloatField(max_length=30)
    bank_name = models.CharField(max_length=40, null=True,blank=True)
    bank_num = models.CharField(max_length=20, null=True,blank=True)
    province = models.CharField(max_length=40, null=True,blank=True)
    trans_date = models.DateTimeField('Transaction date', null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    website = models.URLField('Merchant Website', null=True,blank=True)
    details = models.TextField(max_length=200, null=True,blank=True)

    # def __str__(self):
    #     return self.serializable_value
    
