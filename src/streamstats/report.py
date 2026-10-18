import json
import csv
import os

def save_report(stats, out_path):
    if stats.first_ts:
        first_str = stats.first_ts.isoformat()
    else:
        first_str = None
    if stats.last_ts:
        last_str = stats.last_ts.isoformat()
    else:
        last_str = None
    data = {
        "total_events": stats.total,
        "skipped_lines": stats.skipped,
        "levels": stats.levels,
        "sources": stats.sources,
        "top_errors": dict(stats.get_top_errors()),
        "first_timestamp": first_str,
        "last_timestamp": last_str
    }
    ext = os.path.splitext(out_path)[1]
    if ext.lower() == '.csv':
        with open(out_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["метрика", "значение"])
            writer.writerow(["общее число событий", data["total_events"]])
            writer.writerow(["пропущенные строки", data["skipped_lines"]])
            writer.writerow(["первая временная метка", data["first_timestamp"]])
            writer.writerow(["последняя временная метка", data["last_timestamp"]])
            for level, count in data["levels"].items():
                writer.writerow([f"уровень {level}", count])
            for source, count in data["sources"].items():
                writer.writerow([f"источник {source}", count])
            for err_source, count in data["top_errors"].items():
                writer.writerow([f"частая ошибка {err_source}", count])
    else:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)