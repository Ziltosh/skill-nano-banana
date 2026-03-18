"""Tests for model selection in generate_image."""

import json
from unittest.mock import MagicMock, patch

from src.generate import generate_image


def _create_models_file(tmp_path):
    p = tmp_path / "models.json"
    data = {
        "flash": "gemini-2.5-flash-image",
        "pro": "gemini-3-pro-image-preview",
        "_default": "flash",
    }
    p.write_text(json.dumps(data))
    return p


def _mock_success(mock_genai):
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
    return mock_client


@patch("src.generate.genai")
def test_model_pro_uses_correct_id(mock_genai, tmp_path):
    models_file = _create_models_file(tmp_path)
    mock_client = _mock_success(mock_genai)

    result = generate_image(
        prompt="test",
        api_key="key",
        model="pro",
        output_dir=tmp_path,
        models_file=models_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert result["model"] == "gemini-3-pro-image-preview"
    call_args = mock_client.models.generate_content.call_args
    assert call_args.kwargs["model"] == "gemini-3-pro-image-preview"


@patch("src.generate.genai")
def test_no_model_uses_default(mock_genai, tmp_path):
    models_file = _create_models_file(tmp_path)
    _mock_success(mock_genai)

    result = generate_image(
        prompt="test",
        api_key="key",
        output_dir=tmp_path,
        models_file=models_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert result["model"] == "gemini-2.5-flash-image"


@patch("src.generate.genai")
def test_unknown_model_error(mock_genai, tmp_path):
    models_file = _create_models_file(tmp_path)

    result = generate_image(
        prompt="test",
        api_key="key",
        model="nonexistent",
        output_dir=tmp_path,
        models_file=models_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is False
    assert result["code"] == "UNKNOWN_MODEL"
    assert "flash" in result["error"]
    assert "pro" in result["error"]
