"""Функции для получения справочной информации."""
from collections.abc import Iterable

import httpx

from amoex import client, request_helpers
from amoex.request_helpers import SECURITIES, SERIES


async def get_reference(
    http_client: httpx.AsyncClient,
    placeholder: str = "boards"
) -> client.Table:
    """Получить перечень доступных значений плейсхолдера в адресе запроса.

    Например в описание запроса https://iss.moex.com/iss/reference/32 присутствует следующий адрес
    /iss/engines/[engine]/markets/[market]/boards/[board]/securities с плейсхолдерами engines, markets и
    boards.

    Описание запроса - https://iss.moex.com/iss/reference/28

    :param http_client:
        Http клиент.
    :param placeholder:
        Наименование плейсхолдера в адресе запроса: engines, markets, boards, boardgroups, durations,
        securitytypes, securitygroups, securitycollections.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(ending="index")
    return await request_helpers.get_short_data(http_client, url, placeholder)


async def find_securities(
    http_client: httpx.AsyncClient,
    string: str,
    columns: Iterable[str] | None = ("secid", "regnumber"),
) -> client.Table:
    """Найти инструменты по части Кода, Названию, ISIN, Идентификатору Эмитента, Номеру гос.регистрации.

    Один из вариантов использования - по регистрационному номеру узнать предыдущие тикеры эмитента, и с
    помощью нескольких запросов об истории котировок собрать длинную историю с использованием всех
    предыдущих тикеров.

    Описание запроса - https://iss.moex.com/iss/reference/5

    :param http_client:
        Http клиент.
    :param string:
        Часть Кода, Названия, ISIN, Идентификатора Эмитента, Номера гос.регистрации.
    :param columns:
        Кортеж столбцов, которые нужно загрузить - по умолчанию тикер и номер государственно регистрации.
        Если пустой или None, то загружаются все столбцы.

    :return: Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(ending=SECURITIES)
    table = SECURITIES
    query = request_helpers.make_query(question=string, table=table, columns=columns)
    return await request_helpers.get_short_data(http_client, url, table, query)


async def get_statistics_series(
    http_client: httpx.AsyncClient,
    asset_code: str | None = None,
    show_expired: bool | None = True,
    market: str = 'forts',
    engine: str = 'futures',
) -> client.Table:
    """Получить список статистики


    https://iss.moex.com/iss/reference/151

    :param http_client:
        HTTP клиент.
    :param asset_code:
        Код базового актива
    :param show_expired:
        Показывать уже не торгующиеся серии
    :param market:
        Рынок - по умолчанию акции.
    :param engine:
        Движок - по умолчанию акции.

    :return:
        Список словарей, которые напрямую конвертируется в pandas.DataFrame.
    """
    url = request_helpers.make_url(
        statistics=True,
        history=False,
        engine=engine,
        market=market,
        ending=SERIES,
    )
    table = SERIES
    query = request_helpers.make_query()
    if asset_code:
        query["asset_code"] = asset_code
    if show_expired:
        query["show_expired"] = 1
    return await request_helpers.get_short_data(http_client, url, table, query)
