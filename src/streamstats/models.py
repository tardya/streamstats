from datetime import datetime
from .errors import InvalidEvent, InvalidTimestamp

LVL = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

class Event:
    def __init__(self, timestamp, level, source, message):
        try:
            self.timestamp = datetime.fromisoformat(str(timestamp))
        except (ValueError, TypeError):
            raise InvalidTimestamp(f"неверная метка времени: {timestamp}")
        if level not in LVL:
            raise InvalidEvent(f"неверный уровень: {level}")
        if not source:
            raise InvalidEvent("источник не может быть пустым")

        self.level = level
        self.source = str(source)
        self.message = str(message)