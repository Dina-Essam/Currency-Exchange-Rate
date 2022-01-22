from rest_framework import serializers
from .models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ExchangeRateSerializer(serializers.ModelSerializer):
    To_Currency = serializers.CharField(source='To.symbol')
    From_Currency = serializers.CharField(source='From.symbol')

    class Meta:
        model = ExchangeRate
        fields = ('rate', 'date','To_Currency','From_Currency')
