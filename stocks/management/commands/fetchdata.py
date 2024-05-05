from datetime import datetime, timedelta
from django.db import connection

import yfinance as yahooFinance
from django.core.management.base import BaseCommand

from stocks.models import HistoricalPrice, Stock


class Command(BaseCommand):

    help = "Fetches stock data"

    def handle(self, *args, **kwargs):
        symbols = ["AAPL", "AMZN", "TSLA", "MSFT"]
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=365)  # 1 Year ago
        print("Fetching Data")
        for symbol in symbols:
            print(f"Fetching Ticker for {symbol}")
            stock = yahooFinance.Ticker(symbol)

            data = stock.history(start=start_date, end=end_date)
            stock, _ = Stock.objects.get_or_create(
                symbol=symbol,
                company_name=stock.info["shortName"],
                exchange=stock.info["exchange"],
            )

            print(f"Stock object added for {symbol}")

            print("Overwriting old rows for the historical data...")
            HistoricalPrice.objects.filter(date__gte=start_date, date__lte=end_date, symbol=stock).delete()
            objects_to_add = []
            for index, row in data.iterrows():
                objects_to_add.append(
                    HistoricalPrice(
                        symbol=stock,
                        date=index,
                        open=row["Open"],
                        high=row["High"],
                        low=row["Low"],
                        close=row["Close"],
                        volume=row["Volume"],
                    )
                )
            objs = HistoricalPrice.objects.bulk_create(objects_to_add)
            print(f"{len(objs)} records updated in HistoricalPrice for {symbol}")

        num_queries = len(connection.queries)
        self.stdout.write(self.style.SUCCESS(f"History Updated Successfully in {num_queries} queries"))
