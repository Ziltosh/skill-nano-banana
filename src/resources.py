import json
from pathlib import Path

RESOURCES_DIR = Path.cwd() / "resources"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def list_tags(resources_dir: Path | None = None) -> list[str]:
    """List available resource tags (subdirectory names)."""
    d = resources_dir or RESOURCES_DIR
    if not d.exists():
        return []
    return sorted(
        p.name for p in d.iterdir() if p.is_dir() and not p.name.startswith(".")
    )


def load_tag(
    tag: str, resources_dir: Path | None = None
) -> tuple[list[Path], str | None]:
    """Load images and optional prompt from a resource tag.

    Returns (image_paths, prompt_text_or_none).
    Raises ValueError if tag doesn't exist or has no images.
    """
    d = resources_dir or RESOURCES_DIR
    tag_dir = d / tag

    if not tag_dir.exists() or not tag_dir.is_dir():
        available = list_tags(resources_dir)
        raise ValueError(
            f"Resource tag '{tag}' not found. "
            f"Available tags: {', '.join(available) or 'none'}"
        )

    images = sorted(
        p for p in tag_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not images:
        raise ValueError(
            f"Resource tag '{tag}' has no images "
            f"(expected .png, .jpg, .webp files)"
        )

    # Read optional meta.json
    prompt = None
    meta_file = tag_dir / "meta.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            prompt = meta.get("prompt")

    return images, prompt
