# Analytics module
from app.analytics.data_loader import (
    get_historical_data,
    get_data_by_origen,
    get_data_by_date_range,
    get_latest_by_origen,
    get_all_origenes,
)

__all__ = [
    "get_historical_data",
    "get_data_by_origen",
    "get_data_by_date_range",
    "get_latest_by_origen",
    "get_all_origenes",
]
