import csv
import json

from .errors import InvalidEvent
from .errors import UnsupportedFormat

PARSER_REGISTRY = {}

def register_parser(extension):
    """Декоратор для регистрация парсеров"""
    def decorator(func):
        PARSER_REGISTRY[extension] = func
        return func
    return decorator

def get_parser(extension):
    """Достает парсер из словаря"""
    if extension not in PARSER_REGISTRY:
        raise UnsupportedFormat(f"Неподдерживаемый формат входного файла: {extension}")
    return PARSER_REGISTRY[extension]

@register_parser("csv")
def prs_csv(file):
    reader = csv.DictReader(file)
    yield from enumerate(reader, start=2)

@register_parser("jsonl")
def prs_jsonl(file):
    for i, line in enumerate(file, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            yield i, json.loads(line)
        except json.JSONDecodeError as e:
            raise InvalidEvent(f"Некорректный JSON: {e}")