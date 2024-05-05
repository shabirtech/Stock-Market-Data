from django.urls import include, path

from .views import HistoricalPriceList, StockPerformanceView

urlpatterns = [
    path(
        "stocks/historical-prices/",
        HistoricalPriceList.as_view(),
        name="historical-price-list",
    ),
    path("stocks/<str:symbol>/", StockPerformanceView.as_view(), name="stock-performance"),
]
