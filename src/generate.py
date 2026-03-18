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
from src.models import get_default_model, get_model_id, list_models
from src.resources import list_tags, load_tag
from src.slugify import slugify, unique_path
from src.styles import get_style, list_styles

SUPPORTED_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "4:5", "5:4"]
DEFAULT_RATIO = "16:9"

SUPPORTED_SIZES = ["1k", "2k", "4k"]
DEFAULT_SIZE = "1k"
SIZE_MAP = {"1k": "1K", "2k": "2K", "4k": "4K"}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate image via Gemini API",
        epilog='Example: generate "a cat on the moon" --style ghibli --model pro',
    )
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--style", action="append", default=[], help="Style preset name (repeatable)")
    parser.add_argument("--model", help="Model alias (see models.json)")
    parser.add_argument(
        "--include", action="append", default=[], help="Resource tag to include (repeatable)"
    )
    parser.add_argument("--text", help="Text to display on the generated image (case-preserving)")
    parser.add_argument("--ratio", help="Aspect ratio (e.g., 16:9, 1:1, 9:16)")
    parser.add_argument("--size", help="Image resolution (1k, 2k, 4k)")
    parser.add_argument(
        "--images", nargs="*", default=[], help="Reference image file paths"
    )
    return parser.parse_args(argv)


def generate_image(
    prompt: str,
    api_key: str,
    style: list[str] | None = None,
    model: str | None = None,
    text: str | None = None,
    ratio: str | None = None,
    size: str | None = None,
    include_tags: list[str] | None = None,
    image_paths: list[str] | None = None,
    output_dir: Path | None = None,
    styles_file: Path | None = None,
    models_file: Path | None = None,
    resources_dir: Path | None = None,
    history_file: Path | None = None,
) -> dict:
    """Generate an image and return result dict."""
    if output_dir is None:
        output_dir = Path.cwd() / "out"
    if history_file is None:
        history_file = output_dir / "history.jsonl"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve model
    if model:
        model_id = get_model_id(model, path=models_file)
        if model_id is None:
            available = list_models(path=models_file)
            names = [f"{a} (default)" if d else a for a, _, d in available]
            error_msg = (
                f"Unknown model '{model}'. "
                f"Available models: {', '.join(names) or 'none'}"
            )
            return {"success": False, "error": error_msg, "code": "UNKNOWN_MODEL"}
    else:
        _, model_id = get_default_model(path=models_file)

    # Resolve ratio and size with defaults
    ratio = ratio or DEFAULT_RATIO
    size = size or DEFAULT_SIZE

    if ratio not in SUPPORTED_RATIOS:
        error_msg = (
            f"Unknown ratio '{ratio}'. "
            f"Available ratios: {', '.join(SUPPORTED_RATIOS)}"
        )
        return {"success": False, "error": error_msg, "code": "INVALID_RATIO"}

    if size not in SUPPORTED_SIZES:
        error_msg = (
            f"Unknown size '{size}'. "
            f"Available sizes: {', '.join(SUPPORTED_SIZES)}"
        )
        return {"success": False, "error": error_msg, "code": "INVALID_SIZE"}

    # Load resources from --include tags
    resource_images: list[Path] = []
    resource_prompts: list[str] = []
    if include_tags:
        for tag in include_tags:
            try:
                images, tag_prompt = load_tag(tag, resources_dir=resources_dir)
                resource_images.extend(images)
                if tag_prompt:
                    resource_prompts.append(tag_prompt)
            except ValueError as e:
                code = "UNKNOWN_TAG" if "not found" in str(e) else "EMPTY_RESOURCES"
                return {"success": False, "error": str(e), "code": code}

    # Build the enriched prompt: user prompt + text instruction + include prompts + style
    enriched_prompt = prompt
    if text:
        enriched_prompt = f'{enriched_prompt}, Write the exact text "{text}" on the image, preserving the exact capitalization'
    if resource_prompts:
        enriched_prompt = f"{enriched_prompt}, {', '.join(resource_prompts)}"
    if style:
        style_texts = []
        for s in style:
            s_text = get_style(s, path=styles_file)
            if s_text is None:
                available = list_styles(path=styles_file)
                error_msg = (
                    f"Unknown style '{s}'. "
                    f"Available styles: {', '.join(available) or 'none'}"
                )
                log_generation(
                    prompt=prompt,
                    output_path="",
                    success=False,
                    style=style,
                    text=text,
                    ratio=ratio,
                    size=size,
                    error=error_msg,
                    history_file=history_file,
                )
                return {"success": False, "error": error_msg, "code": "UNKNOWN_STYLE"}
            style_texts.append(s_text)
        enriched_prompt = f"{enriched_prompt}, {', '.join(style_texts)}"

    # Build contents for the API call
    contents: list = []

    # Add resource images from --include
    for img_path in resource_images:
        try:
            img = Image.open(img_path)
            contents.append(img)
        except Exception as e:
            error_msg = f"Cannot load resource image '{img_path}': {e}"
            return {"success": False, "error": error_msg, "code": "IMAGE_ERROR"}

    # Add reference images from --images (chat)
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
                    text=text,
                    error=error_msg,
                    history_file=history_file,
                )
                return {"success": False, "error": error_msg, "code": "IMAGE_ERROR"}

    contents.append(enriched_prompt)

    # Call Gemini API
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_id,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"],
                image_config=types.ImageConfig(
                    aspect_ratio=ratio,
                    image_size=SIZE_MAP[size],
                ),
            ),
        )
    except Exception as e:
        error_msg = f"Gemini API error: {e}"
        log_generation(
            prompt=prompt,
            output_path="",
            success=False,
            style=style,
            text=text,
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
            text=text,
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
        model=model_id,
        text=text,
        ratio=ratio,
        size=size,
        history_file=history_file,
    )

    return {
        "success": True,
        "path": str(output_path.absolute()),
        "prompt": enriched_prompt,
        "style": style,
        "model": model_id,
        "text": text,
        "ratio": ratio,
        "size": size,
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
        style=args.style if args.style else None,
        model=args.model,
        text=args.text if args.text else None,
        ratio=args.ratio if args.ratio else None,
        size=args.size if args.size else None,
        include_tags=args.include if args.include else None,
        image_paths=args.images if args.images else None,
    )

    print(json.dumps(result, ensure_ascii=False))
    if not result["success"]:
        code = result.get("code", "")
        if code == "INVALID_ARGS":
            sys.exit(3)
        elif code in ("UNKNOWN_MODEL", "UNKNOWN_TAG", "EMPTY_RESOURCES", "INVALID_RATIO", "INVALID_SIZE"):
            sys.exit(4)
        else:
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
