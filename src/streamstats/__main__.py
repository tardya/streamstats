import argparse
import logging
import sys

from .analysis import Stats
from .errors import StreamStatsError
from .models import Event
from .parsers import PARSER_REGISTRY
from .parsers import get_parser
from .report import save_report
from .report import save_report_csv


def lazy_filter(stream, level=None, source=None, mintime=None, maxtime=None):
    """Ленивый фильтр потока данных"""
    for line_num, row in stream:
        if level and row.get("level") != level:
            continue
        if source and row.get("source") != source:
            continue
        if mintime and row.get("timestamp") < mintime:
            continue
        if maxtime and row.get("timestamp") > maxtime:
            continue
        yield line_num, row

def main():
    parser = argparse.ArgumentParser(prog="streamstats", description="Потоковый анализатор")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Анализ логов")
    analyze_parser.add_argument("files", nargs="+", metavar="INPUT", help="входные файлы")
    analyze_parser.add_argument("--format", required=True, choices=list(PARSER_REGISTRY.keys()), help="формат файлов")
    analyze_parser.add_argument("--output", default="REPORT.json", help="файл отчета JSON")
    analyze_parser.add_argument("--skip-invalid", action="store_true", help="пропускать ошибочные строки")

    analyze_parser.add_argument("--output-csv", help="сохранение отчета в CSV формат")
    analyze_parser.add_argument("--level", help="фильтр по уровню")
    analyze_parser.add_argument("--source", help="фильтр по источнику")
    analyze_parser.add_argument("--time-from", help="фильтр по началу")
    analyze_parser.add_argument("--time-to", help="фильтр по концу")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="WARNING: %(message)s")
    stats = Stats()
    try:
        parse_func = get_parser(args.format)
    except StreamStatsError as e:
        print(f"Ошибка конфигурации CLI: {e}")
        sys.exit(2)
    for file_idx, filepath in enumerate(args.files, start=1):
        try:
            with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
                stream = parse_func(f)

                if any([args.level, args.source, args.time_from, args.time_to]):
                    stream = lazy_filter(stream, args.level, args.source, args.time_from, args.time_to)

                for line_num, row in stream:
                    try:
                        if not isinstance(row, dict) or not all(k in row for k in ("timestamp", "level", "source", "message")):
                            raise StreamStatsError("Отсутствуют обязательные поля")
                        event = Event(
                            row["timestamp"],
                            row["level"],
                            row["source"],
                            row["message"]
                        )
                        stats.add_event(event)
                    except StreamStatsError as e:
                        if args.skip_invalid:
                            logging.getLogger(__name__).warning(f"Пропущена строка в {filepath}:{line_num}\n{e}")
                            stats.add_skipped()
                        else:
                            print(f"Ошибка в файле {file_idx} ({filepath}), строка {line_num}: {e}", file=sys.stderr)
                            sys.exit(2)
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден - {filepath}")
            sys.exit(2)
    save_report(stats, args.output)
    print(f"JSON-отчет сохранен в: {args.output}")
    if args.output_csv:
        save_report_csv(stats, args.output_csv)
        print(f"CSV-отчет сохранен в: {args.output_csv}")

if __name__ == "__main__":
    main()