import re
import unicodedata
from pathlib import Path

STOP_WORDS = frozenset(
    # French
    "un une le la les de du des en et ou mais dans sur pour par avec sans"
    " ce cette ces qui que quoi dont où au aux se ne pas plus très bien"
    " mon ton son ma ta sa mes tes ses notre votre leur nos vos leurs"
    " je tu il elle on nous vous ils elles me te lui y en ai est"
    " être avoir faire aller dire pouvoir vouloir devoir falloir"
    " tout tous toute toutes même aussi encore entre autre autres"
    " comme car donc si ni peu très trop ici là alors ainsi après avant"
    " chez vers pendant depuis sous selon contre parmi dessus dessous"
    " quelque chaque aucun certains plusieurs tel tels telle telles"
    " magnifique superbe beau belle joli jolie petit petite grand grande"
    .split()
    # English
    + "a an the and or but in on at to for with from by of is are was were"
    " be been being have has had do does did will would shall should"
    " can could may might must not no nor so if than that this these those"
    " it its he she they them their his her my your our me you we us"
    " who what which where when how all each every some any many much"
    " very too also just about into over after before between through"
    " during without again further then once here there up down out off"
    " own same such only other more most"
    .split()
)


def extract_keywords(text: str, max_words: int = 4) -> str:
    """Extract meaningful keywords from text, filtering out stop words."""
    words = re.sub(r"[^a-zA-ZÀ-ÿ0-9]+", " ", text).lower().split()
    keywords = [w for w in words if w not in STOP_WORDS]
    return " ".join(keywords[:max_words])


def strip_image_extension(name: str) -> str:
    """Strip known image extensions from end of string."""
    lower = name.lower()
    for ext in (".png", ".jpeg", ".jpg", ".gif", ".webp"):
        if lower.endswith(ext):
            return name[: -len(ext)]
    return name


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
