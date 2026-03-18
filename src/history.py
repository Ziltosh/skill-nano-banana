import json
from datetime import datetime, timezone
from pathlib import Path


def log_generation(
    prompt: str,
    output_path: str,
    success: bool,
    style: str | None = None,
    model: str | None = None,
    error: str | None = None,
    history_file: Path | None = None,
) -> None:
    """Append a generation log entry to the history file."""
    if history_file is None:
        history_file = Path.cwd() / "out" / "history.jsonl"

    history_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "style": style,
        "model": model,
        "output": output_path,
        "success": success,
        "error": error,
    }

    with open(history_file, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
