from tinydb.queries import QueryLike
from tinydb.table import Table


def table_get(table: Table, condition: QueryLike, default: dict = None):
    """
    Gets document from table.
    If document does not exist, it returns the default value.

    :param table:
    :param condition:
    :param default:
    :return:
    """
    value = table.get(condition)
    if value is None:
        return default
    return value
