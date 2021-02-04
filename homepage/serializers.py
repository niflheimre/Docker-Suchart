from rest_framework import serializers
from homepage.models import case


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = case
        fields = ('name',
                  'nat_id',
                  'goods',
                  'price',
                  'bank_name',
                  'bank_num',
                  'province',
                  'trans_date',
                  'report_date',
                  'website',
                  'details')
        
