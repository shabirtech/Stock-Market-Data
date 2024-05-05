#!/bin/bash

# Run black command
black stock_market_data stocks manage.py

# Run isort command
isort stock_market_data stocks manage.py
