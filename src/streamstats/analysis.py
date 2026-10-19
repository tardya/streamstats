from collections import Counter

from .models import Event


class Stats:
    """Класс для агрегации статистики по потоку событий."""

    def __init__(self):
        self.total_events: int = 0
        self.skipped_lines: int = 0
        self.first_timestamp: str | None = None
        self.last_timestamp: str | None = None
        self.levels: Counter = Counter()
        self.sources: Counter = Counter()
        self._error_sources: Counter = Counter()

    def add_event(self, event: Event) -> None:
        """Добавляет валидное событие в общую статистику."""
        self.total_events += 1
        self.levels[event.level] += 1
        self.sources[event.source] += 1

        if event.level in {"ERROR", "CRITICAL"}:
            self._error_sources[event.source] += 1

        if self.first_timestamp is None or event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp
        if self.last_timestamp is None or event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp

    def add_skipped(self) -> None:
        """Увеличивает счетчик пропущенных ошибочных строк."""
        self.skipped_lines += 1

    def get_top_errors(self) -> dict[str, int]:
        """Возвращает топ-5 источников с наибольшим числом ошибок (ERROR, CRITICAL)."""
        return dict(self._error_sources.most_common(5))