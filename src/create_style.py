"""Create or replace a style preset."""

import argparse
import json
import re
import sys
from pathlib import Path

from src.styles import add_style, get_style

STYLES_FILE = Path.cwd() / "styles.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new style preset")
    parser.add_argument("name", help="Style name (kebab-case)")
    parser.add_argument("description", help="Style prompt text")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing style"
    )
    return parser.parse_args(argv)


def create_style(
    name: str,
    description: str,
    force: bool = False,
    styles_file: Path | None = None,
) -> dict:
    """Create or replace a style preset. Returns result dict."""
    path = styles_file or STYLES_FILE

    # Validate kebab-case
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        return {
            "success": False,
            "error": f"Invalid style name '{name}'. Use kebab-case (e.g., 'my-style').",
            "code": "INVALID_NAME",
        }

    # Check for conflict
    existing = get_style(name, path=path)
    if existing and not force:
        return {
            "success": False,
            "error": f"Style '{name}' already exists",
            "code": "STYLE_EXISTS",
            "existing_prompt": existing,
        }

    success, action = add_style(name, description, force=force, path=path)

    return {
        "success": True,
        "action": action,
        "name": name,
        "prompt_text": description,
    }


def main():
    args = parse_args()
    result = create_style(
        name=args.name,
        description=args.description,
        force=args.force,
    )

    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else (2 if result.get("code") == "STYLE_EXISTS" else 1))


if __name__ == "__main__":
    main()
