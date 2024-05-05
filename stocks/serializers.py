from rest_framework import serializers

from .models import HistoricalPrice, Stock


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ["symbol", "company_name", "exchange"]


class HistoricalPriceSerializer(serializers.ModelSerializer):
    symbol = StockSerializer()

    class Meta:
        model = HistoricalPrice
        fields = ["symbol", "date", "open", "high", "low", "close", "volume"]
