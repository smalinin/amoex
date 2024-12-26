"""Функции для получения информации о свечках."""

from collections.abc import Iterable
import httpx

from amoex import client, request_helpers
from amoex.request_helpers import (
    CANDLE_BORDERS,
    CANDLES,
    DEFAULT_BOARD,
    DEFAULT_ENGINE,
    DEFAULT_MARKET,
)


CANDLES_M1 = 1
CANDLES_M10 = 10
CANDLES_M60 = 60
CANDLES_D = 24
CANDLES_W = 7
CANDLES_M = 31
CANDLES_Q = 4



async def get_market_candle_borders(
    http_client: httpx.AsyncClient,
    security: str,
    market: str = DEFAULT_MARKET,
    engine: str = DEFAULT_ENGINE,
) -> client.Table:
    """Получить таблицу интервалов доступных дат для всех режимов торгов.

    Описание запроса - https://iss.moex.com/iss/reference/156

    :param client:
        HTTP клиент.
    :param security:
        Тикер ценной бумаги.
    :param market:
        Рынок - по умолчанию акции.
    :param engine:
        Движок - по умолчанию акции.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(
        engine=engine,
        market=market,
        security=security,
        ending=CANDLE_BORDERS,
    )
    table = "borders"
    return await request_helpers.get_short_data(http_client, url, table)


async def get_board_candle_borders(
    http_client: httpx.AsyncClient,
    security: str,
    board: str = DEFAULT_BOARD,
    market: str = DEFAULT_MARKET,
    engine: str = DEFAULT_ENGINE,
) -> client.Table:
    """Получить таблицу интервалов доступных дат для указанного режиме торгов.

    Описание запроса - https://iss.moex.com/iss/reference/48

    :param client:
        HTTP клиент.
    :param security:
        Тикер ценной бумаги
    :param board:
        Режим торгов - по умолчанию основной режим торгов T+2.
    :param market:
        Рынок - по умолчанию акции.
    :param engine:
        Движок - по умолчанию акции.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame
    """
    url = request_helpers.make_url(
        engine=engine,
        market=market,
        board=board,
        security=security,
        ending=CANDLE_BORDERS,
    )
    table = "borders"
    return await request_helpers.get_short_data(http_client, url, table)


async def get_market_candles(
    http_client: httpx.AsyncClient,
    security: str,
    interval: int = 24,
    start: str | None = None,
    end: str | None = None,
    market: str = DEFAULT_MARKET,
    engine: str = DEFAULT_ENGINE,
    columns: Iterable[str] | None = ("begin", "open", "high", "low", "close", "volume"),
) -> client.Table:
    """Получить свечи в формате HLOCV указанного инструмента на рынке для основного режима торгов.

    Если торговля идет в нескольких основных режимах, то на один интервал времени может быть выдано
    несколько свечек - по свечке на каждый режим. Предположительно такая ситуация может произойти для
    свечек длиннее 1 дня.

    Описание запроса - https://iss.moex.com/iss/reference/155

    :param client:
        HTTP клиент.
    :param security:
        Тикер ценной бумаги.
    :param interval:
        Размер свечки - целое число 1 (1 минута), 10 (10 минут), 60 (1 час), 24 (1 день), 7 (1 неделя),
        31 (1 месяц) или 4 (1 квартал). По умолчанию дневные данные.
    :param start:
        Дата вида ГГГГ-ММ-ДД. При отсутствии данные будут загружены с начала истории.
    :param end:
        Дата вида ГГГГ-ММ-ДД. При отсутствии данные будут загружены до конца истории.
    :param market:
        Рынок - по умолчанию акции.
    :param engine:
        Движок - по умолчанию акции.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(engine=engine, market=market, security=security, ending=CANDLES)
    table = CANDLES
    query = request_helpers.make_query(interval=interval, start=start, end=end, table=table, columns=columns)
    return await request_helpers.get_long_data(http_client, url, table, query)


async def get_board_candles(
    http_client: httpx.AsyncClient,
    security: str,
    interval: int = 24,
    start: str | None = None,
    end: str | None = None,
    board: str = DEFAULT_BOARD,
    market: str = DEFAULT_MARKET,
    engine: str = DEFAULT_ENGINE,
    columns: Iterable[str] | None = ("begin", "open", "high", "low", "close", "volume"),
) -> client.Table:
    """Получить свечи в формате HLOCV указанного инструмента в указанном режиме торгов за интервал дат.

    Описание запроса - https://iss.moex.com/iss/reference/46

    :param client:
        HTTP клиент.
    :param security:
        Тикер ценной бумаги.
    :param interval:
        Размер свечки - целое число 1 (1 минута), 10 (10 минут), 60 (1 час), 24 (1 день), 7 (1 неделя),
        31 (1 месяц) или 4 (1 квартал). По умолчанию дневные данные.
    :param start:
        Дата вида ГГГГ-ММ-ДД. При отсутствии данные будут загружены с начала истории.
    :param end:
        Дата вида ГГГГ-ММ-ДД. При отсутствии данные будут загружены до конца истории.
    :param board:
        Режим торгов - по умолчанию основной режим торгов T+2.
    :param market:
        Рынок - по умолчанию акции.
    :param engine:
        Движок - по умолчанию акции.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(
        engine=engine,
        market=market,
        board=board,
        security=security,
        ending=CANDLES,
    )
    table = CANDLES
    query = request_helpers.make_query(interval=interval, start=start, end=end, table=table, columns=columns)
    return await request_helpers.get_long_data(http_client, url, table, query)
