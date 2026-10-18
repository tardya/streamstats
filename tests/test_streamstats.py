import io
import json
import subprocess
import sys
from src.streamstats.parsers import prs_csv, prs_jsonl

def test_prs_csv():
    csv_data = "timestamp,level,source,message\n2008-08-01T12:00:00,INFO,App,маевец"
    f = io.StringIO(csv_data)
    lines = list(prs_csv(f))
    assert len(lines) == 1
    assert lines[0][0] == 2
    assert lines[0][1]["message"] == "маевец"


def test_prs_jsonl():
    jsonl_data = '{"timestamp": "2026-10-18T10:48:00", "level": "INFO", "source": "App", "message": "Test"}'
    f = io.StringIO(jsonl_data)
    lines = list(prs_jsonl(f))
    assert len(lines) == 1
    assert lines[0][1]["level"] == "INFO"

def test_empty_file():
    f = io.StringIO("")
    assert len(list(prs_csv(f))) == 0
    assert len(list(prs_jsonl(f))) == 0

def run_cli(*args):
    """функция для эмуляции ввода команд в терминал"""
    cmd = [sys.executable, "-m", "src.streamstats", "analyze"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cli_integration(tmp_path):
    file1 = tmp_path / "log1.csv"
    file1.write_text("timestamp,level,source,message\n2008-08-01T10:00:00,INFO,App,Ок\n", encoding="utf-8")
    file2 = tmp_path / "log2.csv"
    file2.write_text(
        "timestamp,level,source,message\n2026-10-18T10:05:00,BAD_LEVEL,App,Сломано\n2026-10-18T10:10:00,ERROR,DB,Упало",
        encoding="utf-8")
    out_json = tmp_path / "report.json"
    res_strict = run_cli(str(file1), str(file2), "--format", "csv", "--output", str(out_json))
    assert res_strict.returncode == 2
    assert "Ошибка в файле 2" in res_strict.stdout
    res_skip = run_cli(str(file1), str(file2), "--format", "csv", "--output", str(out_json), "--skip-invalid")
    assert res_skip.returncode == 0
    assert "WARNING: Пропущена строка" in res_skip.stderr
    report = json.loads(out_json.read_text(encoding="utf-8"))
    assert report["total_events"] == 2
    assert report["skipped_lines"] == 1