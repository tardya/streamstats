import argparse
import sys
import logging
from .parsers import get_prs
from .analysis import Stats
from .report import save_report
from .errors import StreamStatsError
from .models import Event

def main():
    parser = argparse.ArgumentParser(prog="streamstats", description="потоковый анализатор")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze", help="анализ логов")
    analyze_parser.add_argument("files", nargs="+", metavar="INPUT", help="входные файлы")
    analyze_parser.add_argument("--format", required=True, choices=["csv", "jsonl"], help="формат файлов")
    analyze_parser.add_argument("--output", default="REPORT.json", help="файл отчета (по умолчанию REPORT.json)")
    analyze_parser.add_argument("--skip-invalid", action="store_true", help="пропускать ошибочные строки")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format="WARNING: %(message)s")
    stats = Stats()
    try:
        parse_func = get_prs(args.format)
    except StreamStatsError as e:
        print(f"ошибка конфигурации CLI: {e}")
        sys.exit(2)
    for file_idx, filepath in enumerate(args.files, start=1):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, row in parse_func(f):
                    try:
                        if not all(k in row for k in ("timestamp", "level", "source", "message")):
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
                            logging.warning(f"пропущена строка в {filepath}:{line_num}\n{e}")
                            stats.add_skipped()
                        else:
                            print(f"ошибка в файле {file_idx} ({filepath}), строка {line_num}: {e}")
                            sys.exit(2)
        except FileNotFoundError:
            print(f"ошибка: файл не найден - {filepath}")
            sys.exit(2)
    save_report(stats, args.output)
    print(f"отчет сохранен в: {args.output}")

if __name__ == "__main__":
    main()