from dataclasses import dataclass
from datetime import datetime

from .errors import InvalidEvent
from .errors import InvalidTimestamp

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass
class Event:
    """Модель события с валидацией данных"""

    timestamp: str
    level: str
    source: str
    message: str

    def __post_init__(self):
        """Проверка корректности типов и значений полей"""
        try:
            datetime.fromisoformat(str(self.timestamp))
        except (ValueError, TypeError):
            raise InvalidTimestamp(f"Неверная временная метка: {self.timestamp}")

        if self.level not in VALID_LEVELS:
            raise InvalidEvent(f"Неверное событие: несуществующий уровень {self.level}")

        if not self.source or not str(self.source).strip():
            raise InvalidEvent("Неверное событие: источник не может быть пустым")

        if self.message is None:
            raise InvalidEvent("Неверное событие: сообщение не может быть пустым")

        self.message = str(self.message)