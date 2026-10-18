import csv
import json
from .errors import UnsupportedFormat


def prs_csv(file):
    """генератор для CSV"""
    first_line = file.readline()
    file.seek(0)
    if first_line.count(';') > first_line.count(','):
        delimiter1 = ';'
    else:
        delimiter1 = ','
    reader = csv.DictReader(file, delimiter = delimiter1)
    for num, row in enumerate(reader, start=2):
        yield num, row

def prs_jsonl(file):
    """генератор для JSONL"""
    for num, line in enumerate(file, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            yield num, row
        except json.JSONDecodeError:
            yield num, {}

def get_prs(format_name):
    """возвращает подходящую по формату функцию"""
    registry = {
        "csv": prs_csv,
        "jsonl": prs_jsonl
    }
    if format_name not in registry:
        raise UnsupportedFormat(f"неподдерживаемый формат: {format_name}")
    return registry[format_name]