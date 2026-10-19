from dataclasses import dataclass
from datetime import datetime

from .errors import StreamStatsError

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass
class Event:
    """Модель лог-события с автоматической валидацией данных при создании."""

    timestamp: str
    level: str
    source: str
    message: str

    def __post_init__(self):
        """Проверяет корректность типов и значений полей согласно требованиям."""
        try:
            datetime.fromisoformat(str(self.timestamp))
        except (ValueError, TypeError):
            raise StreamStatsError(f"Неверная временная метка: {self.timestamp}")

        if self.level not in VALID_LEVELS:
            raise StreamStatsError(f"Неверное событие: недопустимый уровень '{self.level}'")

        if not self.source or not str(self.source).strip():
            raise StreamStatsError("Неверное событие: источник (source) не может быть пустым")

        if self.message is None:
            raise StreamStatsError("Неверное событие: сообщение (message) не может быть пустым")

        self.message = str(self.message)