"""Исключения пакета streamstats"""


class StreamStatsError(Exception):
    """Базовый класс для всех ошибок пакета"""


class UnsupportedFormat(StreamStatsError):
    """Неподдерживаемый формат входного файла"""


class InvalidEvent(StreamStatsError):
    """Неверное событие"""


class InvalidTimestamp(StreamStatsError):
    """Неверная временная метка (не ISO 8601)"""


class CLIConfigError(StreamStatsError):
    """Ошибка конфигурации CLI"""