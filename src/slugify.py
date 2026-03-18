import re
import unicodedata
from pathlib import Path


def slugify(text: str, max_length: int = 50) -> str:
    """Convert text to a filesystem-safe slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    if len(text) > max_length:
        text = text[:max_length].rstrip("-")
    return text or "image"


def unique_path(directory: Path, slug: str, ext: str = ".png") -> Path:
    """Return a unique file path, adding numeric suffix if needed."""
    path = directory / f"{slug}{ext}"
    if not path.exists():
        return path
    counter = 2
    while True:
        path = directory / f"{slug}-{counter}{ext}"
        if not path.exists():
            return path
        counter += 1
