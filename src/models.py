import json
from pathlib import Path

MODELS_FILE = Path.cwd() / "models.json"
FALLBACK_MODEL = "gemini-2.5-flash-image"


def _load_models(path: Path | None = None) -> dict[str, str]:
    """Load models from JSON file."""
    p = path or MODELS_FILE
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def get_model_id(alias: str, path: Path | None = None) -> str | None:
    """Get a model's full ID by alias. Returns None if not found."""
    models = _load_models(path)
    if alias.startswith("_"):
        return None
    return models.get(alias)


def get_default_model(path: Path | None = None) -> tuple[str, str]:
    """Get the default model (alias, model_id). Falls back to hardcoded if missing."""
    models = _load_models(path)
    default_alias = models.get("_default", "")
    default_id = models.get(default_alias)
    if default_id:
        return default_alias, default_id
    return "flash", FALLBACK_MODEL


def list_models(path: Path | None = None) -> list[tuple[str, str, bool]]:
    """List available models as (alias, model_id, is_default) tuples."""
    models = _load_models(path)
    default_alias = models.get("_default", "")
    return [
        (alias, model_id, alias == default_alias)
        for alias, model_id in sorted(models.items())
        if not alias.startswith("_")
    ]
