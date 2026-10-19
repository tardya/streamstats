import io
import json
import subprocess
import sys

from src.streamstats.parsers import prs_csv
from src.streamstats.parsers import prs_jsonl


def test_csv():
    csv_data = "timestamp,level,source,message\n2008-08-01T12:00:00,INFO,App,маевец"
    f = io.StringIO(csv_data)
    lines = list(prs_csv(f))
    assert len(lines) == 1
    assert lines[0][0] == 2
    assert lines[0][1]["message"] == "маевец"

def test_jsonl():
    jsonl_data = '{"timestamp": "2026-10-18T10:48:00", "level": "INFO", "source": "App", "message": "Test"}'
    f = io.StringIO(jsonl_data)
    lines = list(prs_jsonl(f))
    assert len(lines) == 1
    assert lines[0][1]["level"] == "INFO"

def test_empty():
    f_csv = io.StringIO("")
    f_jsonl = io.StringIO("")
    assert len(list(prs_csv(f_csv))) == 0
    assert len(list(prs_jsonl(f_jsonl))) == 0

def run_cli(*args):
    cmd = [sys.executable, "-m", "src.streamstats", "analyze"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, check=False)

def test_cli_multiple(tmp_path):
    file1 = tmp_path / "log1.csv"
    file1.write_text("timestamp,level,source,message\n2008-08-01T10:00:00,INFO,App,Ок\n", encoding="utf-8")
    file2 = tmp_path / "log2.csv"
    file2.write_text("timestamp,level,source,message\n2026-10-18T10:10:00,ERROR,DB,Упало\n", encoding="utf-8")
    out_json = tmp_path / "report.json"
    res = run_cli(str(file1), str(file2), "--format", "csv", "--output", str(out_json))
    assert res.returncode == 0
    report = json.loads(out_json.read_text(encoding="utf-8"))
    assert report["total_events"] == 2

def test_cli_strict(tmp_path):
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text(
        "timestamp,level,source,message\n2026-10-18T10:05:00,BAD_LEVEL,App,Сломано\n",
        encoding="utf-8"
    )
    out_json = tmp_path / "report.json"
    res = run_cli(str(bad_file), "--format", "csv", "--output", str(out_json))
    assert res.returncode == 2
    assert "Ошибка в файле 1" in res.stderr

def test_cli_skip_invalid(tmp_path):
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text(
        "timestamp,level,source,message\n2026-10-18T10:05:00,BAD_LEVEL,App,Сломано\n",
        encoding="utf-8"
    )
    out_json = tmp_path / "report.json"
    res = run_cli(str(bad_file), "--format", "csv", "--output", str(out_json), "--skip-invalid")
    assert res.returncode == 0
    assert "WARNING: Пропущена строка" in res.stderr
    report = json.loads(out_json.read_text(encoding="utf-8"))
    assert report["skipped_lines"] == 1