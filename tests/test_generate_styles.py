"""Tests for style application in generate_image."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.generate import generate_image


def _create_styles(tmp_path):
    p = tmp_path / "styles.json"
    p.write_text(json.dumps({"ghibli": "in Studio Ghibli style"}))
    return p


@patch("src.generate.genai")
def test_prompt_enriched_with_style(mock_genai, tmp_path):
    styles_file = _create_styles(tmp_path)

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
        prompt="a castle",
        api_key="test-key",
        style="ghibli",
        output_dir=tmp_path,
        styles_file=styles_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert result["prompt"] == "a castle, in Studio Ghibli style"


@patch("src.generate.genai")
def test_unknown_style_error(mock_genai, tmp_path):
    styles_file = _create_styles(tmp_path)

    result = generate_image(
        prompt="test",
        api_key="test-key",
        style="nonexistent",
        output_dir=tmp_path,
        styles_file=styles_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is False
    assert "Unknown style" in result["error"]
    assert "ghibli" in result["error"]


@patch("src.generate.genai")
def test_no_style_no_enrichment(mock_genai, tmp_path):
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
        prompt="a castle",
        api_key="test-key",
        output_dir=tmp_path,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert result["prompt"] == "a castle"
