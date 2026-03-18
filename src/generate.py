"""Generate images via the Gemini API."""

import argparse
import json
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from src.config import get_api_key
from src.history import log_generation
from src.slugify import slugify, unique_path
from src.styles import get_style, list_styles

MODEL = "gemini-2.5-flash-image"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate image via Gemini API")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--style", help="Style preset name to apply")
    parser.add_argument(
        "--images", nargs="*", default=[], help="Reference image file paths"
    )
    return parser.parse_args(argv)


def generate_image(
    prompt: str,
    api_key: str,
    style: str | None = None,
    image_paths: list[str] | None = None,
    output_dir: Path | None = None,
    styles_file: Path | None = None,
    history_file: Path | None = None,
) -> dict:
    """Generate an image and return result dict."""
    if output_dir is None:
        output_dir = Path.cwd() / "out"
    if history_file is None:
        history_file = output_dir / "history.jsonl"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Build the enriched prompt
    enriched_prompt = prompt
    if style:
        style_text = get_style(style, path=styles_file)
        if style_text is None:
            available = list_styles(path=styles_file)
            error_msg = (
                f"Unknown style '{style}'. "
                f"Available styles: {', '.join(available) or 'none'}"
            )
            log_generation(
                prompt=prompt,
                output_path="",
                success=False,
                style=style,
                error=error_msg,
                history_file=history_file,
            )
            return {"success": False, "error": error_msg, "code": "UNKNOWN_STYLE"}
        enriched_prompt = f"{prompt}, {style_text}"

    # Build contents for the API call
    contents: list = []

    # Add reference images if provided
    if image_paths:
        for img_path in image_paths:
            try:
                img = Image.open(img_path)
                contents.append(img)
            except Exception as e:
                error_msg = f"Cannot load image '{img_path}': {e}"
                log_generation(
                    prompt=prompt,
                    output_path="",
                    success=False,
                    style=style,
                    error=error_msg,
                    history_file=history_file,
                )
                return {"success": False, "error": error_msg, "code": "IMAGE_ERROR"}

    contents.append(enriched_prompt)

    # Call Gemini API
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"]
            ),
        )
    except Exception as e:
        error_msg = f"Gemini API error: {e}"
        log_generation(
            prompt=prompt,
            output_path="",
            success=False,
            style=style,
            error=error_msg,
            history_file=history_file,
        )
        return {"success": False, "error": error_msg, "code": "API_ERROR"}

    # Extract image from response
    generated_image = None
    for part in response.parts:
        if part.inline_data is not None:
            generated_image = part.as_image()
            break

    if generated_image is None:
        error_msg = "No image returned by the API. The prompt may have been rejected."
        log_generation(
            prompt=prompt,
            output_path="",
            success=False,
            style=style,
            error=error_msg,
            history_file=history_file,
        )
        return {"success": False, "error": error_msg, "code": "CONTENT_BLOCKED"}

    # Save image
    slug = slugify(prompt)
    output_path = unique_path(output_dir, slug)
    generated_image.save(str(output_path))

    rel_path = str(output_path)
    log_generation(
        prompt=prompt,
        output_path=rel_path,
        success=True,
        style=style,
        history_file=history_file,
    )

    return {
        "success": True,
        "path": str(output_path.absolute()),
        "prompt": enriched_prompt,
        "style": style,
    }


def main():
    args = parse_args()

    try:
        api_key = get_api_key()
    except SystemExit as e:
        print(json.dumps({"success": False, "error": str(e), "code": "MISSING_KEY"}))
        sys.exit(1)

    result = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        style=args.style,
        image_paths=args.images if args.images else None,
    )

    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else 2)


if __name__ == "__main__":
    main()
