class StreamStatsError(Exception):
    """базовый класс для всех ошибок"""
    pass

class UnsupportedFormat(StreamStatsError):
    """неподдерживаемый формат"""
    pass

class InvalidEvent(StreamStatsError):
    """неверное событие"""
    pass

class InvalidTimestamp(StreamStatsError):
    """неверный формат временной метки (не ISO 8601)"""
    pass

class CLIConfigError(StreamStatsError):
    """ошибка в командной строке"""
    pass