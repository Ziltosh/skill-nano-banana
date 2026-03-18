import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.generate import generate_image, parse_args


class TestParseArgs:
    def test_prompt_only(self):
        args = parse_args(["un chat"])
        assert args.prompt == "un chat"
        assert args.style is None
        assert args.images == []

    def test_with_style(self):
        args = parse_args(["un château", "--style", "ghibli"])
        assert args.prompt == "un château"
        assert args.style == "ghibli"

    def test_with_images(self):
        args = parse_args(["transform", "--images", "a.png", "b.png"])
        assert args.images == ["a.png", "b.png"]

    def test_empty_prompt(self):
        with pytest.raises(SystemExit):
            parse_args([])

    def test_with_text(self):
        args = parse_args(["un logo", "--text", "Hello World"])
        assert args.prompt == "un logo"
        assert args.text == "Hello World"

    def test_without_text(self):
        args = parse_args(["un paysage"])
        assert args.text is None


class TestGenerateImage:
    @patch("src.generate.genai")
    def test_successful_generation(self, mock_genai, tmp_path):
        # Mock the API response
        mock_image = MagicMock()
        mock_image.save = MagicMock()

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
            prompt="un chat",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert "un-chat" in result["path"]
        mock_image.save.assert_called_once()

    @patch("src.generate.genai")
    def test_api_error(self, mock_genai, tmp_path):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API quota exceeded")
        mock_genai.Client.return_value = mock_client

        result = generate_image(
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is False
        assert "API quota exceeded" in result["error"]

    @patch("src.generate.genai")
    def test_no_image_in_response(self, mock_genai, tmp_path):
        mock_part = MagicMock()
        mock_part.text = "I cannot generate that image"
        mock_part.inline_data = None

        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        result = generate_image(
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is False
        assert "No image" in result["error"] or "no image" in result["error"].lower()

    @patch("src.generate.genai")
    def test_history_logged_on_success(self, mock_genai, tmp_path):
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

        history_file = tmp_path / "history.jsonl"
        generate_image(
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=history_file,
        )

        assert history_file.exists()
        entry = json.loads(history_file.read_text().strip())
        assert entry["success"] is True

    @patch("src.generate.genai")
    def test_history_logged_on_failure(self, mock_genai, tmp_path):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("fail")
        mock_genai.Client.return_value = mock_client

        history_file = tmp_path / "history.jsonl"
        generate_image(
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=history_file,
        )

        entry = json.loads(history_file.read_text().strip())
        assert entry["success"] is False

    @patch("src.generate.genai")
    def test_slug_naming(self, mock_genai, tmp_path):
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
            prompt="un paysage montagneux",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert "un-paysage-montagneux" in result["path"]

    @patch("src.generate.genai")
    def test_text_prompt_enrichment(self, mock_genai, tmp_path):
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

        generate_image(
            prompt="un logo",
            api_key="test-key",
            text="ACME CORP",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        contents = call_args.kwargs.get("contents") or call_args[1].get("contents")
        prompt_text = contents[-1]
        assert "ACME CORP" in prompt_text
        assert "exact text" in prompt_text.lower() or "exact capitalization" in prompt_text.lower()

    @patch("src.generate.genai")
    def test_no_text_instruction_without_flag(self, mock_genai, tmp_path):
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

        generate_image(
            prompt="un paysage",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        contents = call_args.kwargs.get("contents") or call_args[1].get("contents")
        prompt_text = contents[-1]
        assert prompt_text == "un paysage"

    @patch("src.generate.genai")
    def test_empty_text_ignored(self, mock_genai, tmp_path):
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

        generate_image(
            prompt="un paysage",
            api_key="test-key",
            text="",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        contents = call_args.kwargs.get("contents") or call_args[1].get("contents")
        prompt_text = contents[-1]
        assert prompt_text == "un paysage"

    @patch("src.generate.genai")
    def test_text_in_result_dict(self, mock_genai, tmp_path):
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
            prompt="un logo",
            api_key="test-key",
            text="HELLO",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert result["text"] == "HELLO"

    @patch("src.generate.genai")
    def test_no_text_in_result_without_flag(self, mock_genai, tmp_path):
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
            prompt="un paysage",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert result.get("text") is None

    @patch("src.generate.genai")
    def test_text_logged_in_history(self, mock_genai, tmp_path):
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

        history_file = tmp_path / "history.jsonl"
        generate_image(
            prompt="test",
            api_key="test-key",
            text="TEST",
            output_dir=tmp_path,
            history_file=history_file,
        )

        entry = json.loads(history_file.read_text().strip())
        assert entry["text"] == "TEST"
