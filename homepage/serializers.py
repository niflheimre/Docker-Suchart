from rest_framework import serializers
from homepage.models import case,Tweet


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
                  'details',
                  'status')
        
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('user',
                  'post',
                  'status')
