import csv
import json

from collections.abc import Callable
from collections.abc import Iterator
from typing import Any

from .errors import StreamStatsError

PARSER_REGISTRY: dict[str, Callable] = {}

def register_parser(format_name: str):
    """Декоратор для регистрации функций-парсеров."""
    def decorator(func):
        PARSER_REGISTRY[format_name] = func
        return func
    return decorator

@register_parser("csv")
def prs_csv(file_obj) -> Iterator[tuple[int, dict[str, Any]]]:
    reader = csv.DictReader(file_obj)
    yield from enumerate(reader, start=2)

@register_parser("jsonl")
def prs_jsonl(file_obj) -> Iterator[tuple[int, dict[str, Any]]]:
    for i, line in enumerate(file_obj, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            yield i, row
        except json.JSONDecodeError as e:
            raise StreamStatsError(f"Ошибка JSON: {e}")

def get_prs(format_name: str) -> Callable:
    """Получает зарегистрированный парсер по имени формата."""
    if format_name not in PARSER_REGISTRY:
        raise StreamStatsError(f"Неподдерживаемый формат: {format_name}. Доступные: {list(PARSER_REGISTRY.keys())}")
    return PARSER_REGISTRY[format_name]