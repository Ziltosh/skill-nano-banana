"""Tests for image reference handling in generate_image."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from PIL import Image

from src.generate import generate_image


@patch("src.generate.genai")
def test_with_reference_images(mock_genai, tmp_path):
    # Create a test reference image
    ref_img_path = tmp_path / "ref.png"
    Image.new("RGB", (10, 10), color="red").save(ref_img_path)

    mock_image = MagicMock()
    mock_part = MagicMock()
    mock_part.text = None
    mock_part.inline_data = True
    mock_part.as_image.return_value = mock_image

    mock_response = MagicMock()
    mock_response.parts = [mock_part]

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client

    result = generate_image(
        prompt="make it blue",
        api_key="test-key",
        image_paths=[str(ref_img_path)],
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    # Verify the API was called with image + text
    call_args = mock_client.models.generate_content.call_args
    contents = call_args.kwargs.get("contents") or call_args[1].get("contents")
    assert len(contents) == 2  # 1 image + 1 text prompt
    assert isinstance(contents[0], Image.Image)
    assert contents[1] == "make it blue"


@patch("src.generate.genai")
def test_invalid_image_path(mock_genai, tmp_path):
    result = generate_image(
        prompt="test",
        api_key="test-key",
        image_paths=["/nonexistent/image.png"],
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is False
    assert "Cannot load image" in result["error"]


@patch("src.generate.genai")
def test_single_image_output_named_after_image(mock_genai, tmp_path):
    """T005: single reference image: output filename matches image basename."""
    ref_img_path = tmp_path / "mon-logo.png"
    Image.new("RGB", (10, 10), color="red").save(ref_img_path)

    mock_image = MagicMock()
    mock_part = MagicMock()
    mock_part.text = None
    mock_part.inline_data = True
    mock_part.as_image.return_value = mock_image

    mock_response = MagicMock()
    mock_response.parts = [mock_part]

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client

    result = generate_image(
        prompt="make it blue",
        api_key="test-key",
        image_paths=[str(ref_img_path)],
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert "mon-logo" in Path(result["path"]).stem


@patch("src.generate.genai")
def test_single_image_special_chars_slugified(mock_genai, tmp_path):
    """T006: single reference image with special chars: slugified correctly."""
    ref_img_path = tmp_path / "Mon Logo V2!.png"
    Image.new("RGB", (10, 10), color="red").save(ref_img_path)

    mock_image = MagicMock()
    mock_part = MagicMock()
    mock_part.text = None
    mock_part.inline_data = True
    mock_part.as_image.return_value = mock_image

    mock_response = MagicMock()
    mock_response.parts = [mock_part]

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client

    result = generate_image(
        prompt="modify",
        api_key="test-key",
        image_paths=[str(ref_img_path)],
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    stem = Path(result["path"]).stem
    assert "mon-logo-v2" in stem
    assert "!" not in stem


@patch("src.generate.genai")
def test_single_image_in_subdir_uses_basename(mock_genai, tmp_path):
    """T007: single reference image in subdirectory: only basename used."""
    subdir = tmp_path / "photos"
    subdir.mkdir()
    ref_img_path = subdir / "vacances-2024.jpg"
    Image.new("RGB", (10, 10), color="red").save(ref_img_path)

    mock_image = MagicMock()
    mock_part = MagicMock()
    mock_part.text = None
    mock_part.inline_data = True
    mock_part.as_image.return_value = mock_image

    mock_response = MagicMock()
    mock_response.parts = [mock_part]

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client

    result = generate_image(
        prompt="enhance",
        api_key="test-key",
        image_paths=[str(ref_img_path)],
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert "vacances-2024" in Path(result["path"]).stem
    assert "photos" not in Path(result["path"]).stem


@patch("src.generate.genai")
def test_no_images_falls_back_to_text_only(mock_genai, tmp_path):
    mock_image = MagicMock()
    mock_part = MagicMock()
    mock_part.text = None
    mock_part.inline_data = True
    mock_part.as_image.return_value = mock_image

    mock_response = MagicMock()
    mock_response.parts = [mock_part]

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client

    result = generate_image(
        prompt="a landscape",
        api_key="test-key",
        image_paths=None,
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    call_args = mock_client.models.generate_content.call_args
    contents = call_args.kwargs.get("contents") or call_args[1].get("contents")
    assert len(contents) == 1  # text only
