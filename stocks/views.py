from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HistoricalPrice, Stock
from .serializers import HistoricalPriceSerializer


class HistoricalPriceList(APIView):

    def get(self, request):
        queryset = HistoricalPrice.objects.all().order_by("-date")
        serializer = HistoricalPriceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HistoricalPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockPerformanceView(APIView):
    def get(self, request, symbol):
        try:
            stock = Stock.objects.get(symbol=symbol)
            historical_prices = HistoricalPrice.objects.filter(symbol=stock).order_by("-date")

            current_date = datetime.today().date()
            weekly_performance = self.calculate_performance(historical_prices, current_date, timedelta(days=7))
            monthly_performance = self.calculate_performance(historical_prices, current_date, timedelta(days=30))
            quarterly_performance = self.calculate_performance(historical_prices, current_date, timedelta(days=90))
            six_months_performance = self.calculate_performance(historical_prices, current_date, timedelta(days=180))
            yearly_performance = self.calculate_performance(historical_prices, current_date, timedelta(days=365))

            response_data = {
                "symbol": stock.symbol,
                "weekly_performance": weekly_performance,
                "monthly_performance": monthly_performance,
                "quarterly_performance": quarterly_performance,
                "six_months_performance": six_months_performance,
                "yearly_performance": yearly_performance,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response(
                {"error": f"Stock with symbol '{symbol}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def calculate_performance(self, historical_prices, current_date, delta):
        start_date = current_date - delta
        prices_in_range = historical_prices.filter(date__gte=start_date)
        if prices_in_range.exists():
            start_price = prices_in_range.last().close
            current_price = prices_in_range.first().close
            return ((current_price - start_price) / start_price) * 100
        else:
            return None
