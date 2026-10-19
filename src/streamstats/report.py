import csv
import json

from .analysis import Stats


def save_report(stats: Stats, filepath: str):
    """Сохраняет сводную статистику в формате JSON."""
    report_data = {
        "total_events": stats.total_events,
        "skipped_lines": stats.skipped_lines,
        "first_timestamp": stats.first_timestamp,
        "last_timestamp": stats.last_timestamp,
        "levels": stats.levels,
        "sources": stats.sources,
        "top_errors": stats.get_top_errors()
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)


def save_report_csv(stats: Stats, filepath: str):
    """Сохраняет сводную статистику в формате CSV без дублирования расчетов."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Метрика", "Значение"])
        writer.writerow(["Всего событий", stats.total_events])
        writer.writerow(["Пропущено строк", stats.skipped_lines])
        writer.writerow(["Первое событие", stats.first_timestamp or "N/A"])
        writer.writerow(["Последнее событие", stats.last_timestamp or "N/A"])
        writer.writerow([])

        writer.writerow(["Статистика по уровням", ""])
        for lvl, count in stats.levels.items():
            writer.writerow([lvl, count])

        writer.writerow([])
        writer.writerow(["Топ-5 источников ошибок", ""])
        for source, count in stats.get_top_errors().items():
            writer.writerow([source, count])