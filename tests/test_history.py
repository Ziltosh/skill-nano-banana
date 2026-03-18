import json

from src.history import log_generation


def test_append_entry(tmp_path):
    history_file = tmp_path / "history.jsonl"
    log_generation(
        prompt="un chat",
        output_path="out/un-chat.png",
        success=True,
        history_file=history_file,
    )
    lines = history_file.read_text().strip().split("\n")
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["prompt"] == "un chat"
    assert entry["output"] == "out/un-chat.png"
    assert entry["success"] is True
    assert entry["style"] is None
    assert entry["error"] is None
    assert "timestamp" in entry


def test_append_with_style(tmp_path):
    history_file = tmp_path / "history.jsonl"
    log_generation(
        prompt="a castle",
        output_path="out/a-castle.png",
        success=True,
        style="ghibli",
        history_file=history_file,
    )
    entry = json.loads(history_file.read_text().strip())
    assert entry["style"] == "ghibli"


def test_append_failure(tmp_path):
    history_file = tmp_path / "history.jsonl"
    log_generation(
        prompt="test",
        output_path="",
        success=False,
        error="API error",
        history_file=history_file,
    )
    entry = json.loads(history_file.read_text().strip())
    assert entry["success"] is False
    assert entry["error"] == "API error"


def test_creates_parent_directory(tmp_path):
    history_file = tmp_path / "subdir" / "history.jsonl"
    log_generation(
        prompt="test",
        output_path="out/test.png",
        success=True,
        history_file=history_file,
    )
    assert history_file.exists()


def test_multiple_entries(tmp_path):
    history_file = tmp_path / "history.jsonl"
    for i in range(3):
        log_generation(
            prompt=f"prompt {i}",
            output_path=f"out/prompt-{i}.png",
            success=True,
            history_file=history_file,
        )
    lines = history_file.read_text().strip().split("\n")
    assert len(lines) == 3
    for i, line in enumerate(lines):
        entry = json.loads(line)
        assert entry["prompt"] == f"prompt {i}"
