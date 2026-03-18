import json
from pathlib import Path

STYLES_FILE = Path.cwd() / "styles.json"


def _load_styles(path: Path | None = None) -> dict[str, str]:
    """Load styles from JSON file."""
    p = path or STYLES_FILE
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def _save_styles(styles: dict[str, str], path: Path | None = None) -> None:
    """Save styles to JSON file."""
    p = path or STYLES_FILE
    with open(p, "w") as f:
        json.dump(styles, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_style(name: str, path: Path | None = None) -> str | None:
    """Get a style's prompt text by name. Returns None if not found."""
    return _load_styles(path).get(name)


def list_styles(path: Path | None = None) -> list[str]:
    """List all available style names."""
    return sorted(_load_styles(path).keys())


def add_style(
    name: str, prompt_text: str, force: bool = False, path: Path | None = None
) -> tuple[bool, str]:
    """Add or replace a style. Returns (success, action)."""
    styles = _load_styles(path)
    if name in styles and not force:
        return False, "exists"
    action = "replaced" if name in styles else "created"
    styles[name] = prompt_text
    _save_styles(styles, path)
    return True, action
