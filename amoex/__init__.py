"""Реализация части запросов к MOEX ISS.

Результаты запросов являются списками словарей и могут быть конвертированы в pandas.DataFrame.

Работа функций-запросов базируется на универсальном клиенте, позволяющем осуществлять произвольные
запросы к ISS MOEX, поэтому перечень доступных функций-запросов может быть при необходимости дополнен:

- Полный перечень запросов https://iss.moex.com/iss/reference/
- Дополнительное описание https://fs.moex.com/files/6523
"""
from amoex.candles import (
    get_board_candle_borders,
    get_board_candles,
    get_market_candle_borders,
    get_market_candles,
)
from amoex.client import ISSClient, TableRow, TablesDict, Values
from amoex.history import get_board_dates, get_board_history, get_board_securities, get_market_history
from amoex.reference import find_securities, get_reference

__all__ = [
    "get_board_candle_borders",
    "get_board_candles",
    "get_market_candle_borders",
    "get_market_candles",
    "ISSClient",
    "TableRow",
    "TablesDict",
    "Values",
    "get_board_dates",
    "get_board_history",
    "get_board_securities",
    "get_market_history",
    "find_securities",
    "get_reference",
]
