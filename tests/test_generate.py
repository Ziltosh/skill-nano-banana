import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.generate import generate_image, parse_args


class TestParseArgs:
    def test_prompt_only(self):
        args = parse_args(["un chat"])
        assert args.prompt == "un chat"
        assert args.style == []
        assert args.images == []

    def test_with_style(self):
        args = parse_args(["un château", "--style", "ghibli"])
        assert args.prompt == "un château"
        assert args.style == ["ghibli"]

    def test_with_multiple_styles(self):
        args = parse_args(["un chat", "--style", "ghibli", "--style", "pixel-art"])
        assert args.style == ["ghibli", "pixel-art"]

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

    def test_with_ratio(self):
        args = parse_args(["un logo", "--ratio", "1:1"])
        assert args.ratio == "1:1"

    def test_without_ratio(self):
        args = parse_args(["un paysage"])
        assert args.ratio is None

    def test_with_size(self):
        args = parse_args(["un paysage", "--size", "2k"])
        assert args.size == "2k"

    def test_without_size(self):
        args = parse_args(["un paysage"])
        assert args.size is None


class TestParseArgsName:
    def test_with_name(self):
        args = parse_args(["un chat", "--name", "resultat"])
        assert args.name == "resultat"

    def test_without_name(self):
        args = parse_args(["un chat"])
        assert args.name is None


class TestNameForcing:
    @patch("src.generate.genai")
    def test_name_forces_output_filename(self, mock_genai, tmp_path):
        """T011: --name forces output filename."""
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
            prompt="un chat",
            api_key="test-key",
            name="resultat-final",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert "resultat-final" in Path(result["path"]).stem

    @patch("src.generate.genai")
    def test_name_priority_over_images(self, mock_genai, tmp_path):
        """T012: --name takes priority over single --images."""
        from PIL import Image as PILImage

        ref_img = tmp_path / "logo.png"
        PILImage.new("RGB", (10, 10)).save(ref_img)

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
            prompt="modifie",
            api_key="test-key",
            name="nouveau-logo",
            image_paths=[str(ref_img)],
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert "nouveau-logo" in Path(result["path"]).stem

    @patch("src.generate.genai")
    def test_name_with_image_extension_stripped(self, mock_genai, tmp_path):
        """T013: --name with image extension stripped."""
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
            prompt="un chat",
            api_key="test-key",
            name="logo.png",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        stem = Path(result["path"]).stem
        assert stem == "logo"


class TestKeywordNaming:
    @patch("src.generate.genai")
    def test_prompt_without_images_uses_keywords(self, mock_genai, tmp_path):
        """T019: prompt without images: output named with keywords."""
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
            prompt="un chat sur un skateboard",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        stem = Path(result["path"]).stem
        assert "chat" in stem
        assert "skateboard" in stem
        # stop words should not be in the name
        assert stem != "un-chat-sur-un-skateboard"

    @patch("src.generate.genai")
    def test_long_prompt_max_4_keywords(self, mock_genai, tmp_path):
        """T020: long prompt: output name has max 4 keywords."""
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
            prompt="un magnifique paysage de montagne enneigée au coucher du soleil avec des reflets dorés sur un lac cristallin entouré de sapins",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        stem = Path(result["path"]).stem
        # Max 4 keywords, so max 4 segments separated by hyphens
        parts = stem.split("-")
        assert len(parts) <= 4

    @patch("src.generate.genai")
    def test_multiple_images_uses_prompt_keywords(self, mock_genai, tmp_path):
        """T021: multiple reference images: output named with prompt keywords."""
        from PIL import Image as PILImage

        img1 = tmp_path / "chat.png"
        img2 = tmp_path / "chien.png"
        PILImage.new("RGB", (10, 10)).save(img1)
        PILImage.new("RGB", (10, 10)).save(img2)

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
            prompt="fusionne ces deux animaux",
            api_key="test-key",
            image_paths=[str(img1), str(img2)],
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        stem = Path(result["path"]).stem
        # Should use prompt keywords, not image names
        assert "fusionne" in stem or "animaux" in stem

    @patch("src.generate.genai")
    def test_only_stop_words_fallback_image(self, mock_genai, tmp_path):
        """T022: prompt with only stop words: output named image.png (fallback)."""
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
            prompt="un le de la",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        assert result["success"] is True
        assert Path(result["path"]).stem == "image"


class TestRetroCompatibility:
    @patch("src.generate.genai")
    def test_no_images_no_name_uses_keywords(self, mock_genai, tmp_path):
        """T023: no images, no name: output named with prompt keywords."""
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
        stem = Path(result["path"]).stem
        assert "paysage" in stem
        # "un" is a stop word, should not be in name
        assert not stem.startswith("un-")


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
        assert "chat" in result["path"]
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

        assert "paysage-montagneux" in result["path"]

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

    @patch("src.generate.genai")
    def test_ratio_passed_to_image_config(self, mock_genai, tmp_path):
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
            ratio="1:1",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        config = call_args.kwargs["config"]
        assert config.image_config.aspect_ratio == "1:1"

    @patch("src.generate.genai")
    def test_default_ratio_16_9(self, mock_genai, tmp_path):
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
        config = call_args.kwargs["config"]
        assert config.image_config.aspect_ratio == "16:9"

    def test_invalid_ratio_error(self, tmp_path):
        result = generate_image(
            prompt="test",
            api_key="test-key",
            ratio="7:3",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is False
        assert result["code"] == "INVALID_RATIO"
        assert "7:3" in result["error"]
        assert "16:9" in result["error"]

    @patch("src.generate.genai")
    def test_ratio_in_result_dict(self, mock_genai, tmp_path):
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
            prompt="test",
            api_key="test-key",
            ratio="1:1",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["ratio"] == "1:1"

    @patch("src.generate.genai")
    def test_default_ratio_in_result(self, mock_genai, tmp_path):
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
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["ratio"] == "16:9"

    @patch("src.generate.genai")
    def test_ratio_logged_in_history(self, mock_genai, tmp_path):
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
            ratio="9:16",
            output_dir=tmp_path,
            history_file=history_file,
        )
        entry = json.loads(history_file.read_text().strip())
        assert entry["ratio"] == "9:16"

    @patch("src.generate.genai")
    def test_size_passed_to_image_config(self, mock_genai, tmp_path):
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
            size="4k",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        config = call_args.kwargs["config"]
        assert config.image_config.image_size == "4K"

    @patch("src.generate.genai")
    def test_default_size_1k(self, mock_genai, tmp_path):
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
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )

        call_args = mock_client.models.generate_content.call_args
        config = call_args.kwargs["config"]
        assert config.image_config.image_size == "1K"

    def test_invalid_size_error(self, tmp_path):
        result = generate_image(
            prompt="test",
            api_key="test-key",
            size="8k",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is False
        assert result["code"] == "INVALID_SIZE"
        assert "8k" in result["error"]

    @patch("src.generate.genai")
    def test_size_in_result_dict(self, mock_genai, tmp_path):
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
            prompt="test",
            api_key="test-key",
            size="2k",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["size"] == "2k"

    @patch("src.generate.genai")
    def test_size_logged_in_history(self, mock_genai, tmp_path):
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
            size="2k",
            output_dir=tmp_path,
            history_file=history_file,
        )
        entry = json.loads(history_file.read_text().strip())
        assert entry["size"] == "2k"

    @patch("src.generate.genai")
    def test_ratio_and_size_combined_with_style(self, mock_genai, tmp_path):
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

        styles_file = tmp_path / "styles.json"
        styles_file.write_text('{"ghibli": "Ghibli style"}')

        result = generate_image(
            prompt="un poster",
            api_key="test-key",
            ratio="9:16",
            size="2k",
            style=["ghibli"],
            output_dir=tmp_path,
            styles_file=styles_file,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is True
        assert result["ratio"] == "9:16"
        assert result["size"] == "2k"
        assert "Ghibli" in result["prompt"]

        config = mock_client.models.generate_content.call_args.kwargs["config"]
        assert config.image_config.aspect_ratio == "9:16"
        assert config.image_config.image_size == "2K"

    @patch("src.generate.genai")
    def test_ratio_size_and_text_combined(self, mock_genai, tmp_path):
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
            ratio="1:1",
            size="4k",
            text="BRAND",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is True
        assert result["ratio"] == "1:1"
        assert result["size"] == "4k"
        assert "BRAND" in result["prompt"]

    @patch("src.generate.genai")
    def test_multi_style_in_result_dict(self, mock_genai, tmp_path):
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

        styles_file = tmp_path / "styles.json"
        styles_file.write_text('{"ghibli": "Ghibli style", "pixel-art": "pixel art style"}')

        result = generate_image(
            prompt="test",
            api_key="test-key",
            style=["ghibli", "pixel-art"],
            output_dir=tmp_path,
            styles_file=styles_file,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is True
        assert result["style"] == ["ghibli", "pixel-art"]

    @patch("src.generate.genai")
    def test_no_style_result_is_none(self, mock_genai, tmp_path):
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
            prompt="test",
            api_key="test-key",
            output_dir=tmp_path,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["style"] is None

    @patch("src.generate.genai")
    def test_multi_style_logged_in_history(self, mock_genai, tmp_path):
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

        styles_file = tmp_path / "styles.json"
        styles_file.write_text('{"ghibli": "Ghibli style", "pixel-art": "pixel art style"}')

        history_file = tmp_path / "history.jsonl"
        generate_image(
            prompt="test",
            api_key="test-key",
            style=["ghibli", "pixel-art"],
            output_dir=tmp_path,
            styles_file=styles_file,
            history_file=history_file,
        )
        entry = json.loads(history_file.read_text().strip())
        assert entry["style"] == ["ghibli", "pixel-art"]

    @patch("src.generate.genai")
    def test_multi_style_with_text_ratio_size(self, mock_genai, tmp_path):
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

        styles_file = tmp_path / "styles.json"
        styles_file.write_text('{"ghibli": "Ghibli style", "pixel-art": "pixel art style"}')

        result = generate_image(
            prompt="un poster",
            api_key="test-key",
            style=["ghibli", "pixel-art"],
            text="CONCERT",
            ratio="9:16",
            size="2k",
            output_dir=tmp_path,
            styles_file=styles_file,
            history_file=tmp_path / "history.jsonl",
        )
        assert result["success"] is True
        assert result["style"] == ["ghibli", "pixel-art"]
        assert result["text"] == "CONCERT"
        assert result["ratio"] == "9:16"
        assert result["size"] == "2k"
        assert "CONCERT" in result["prompt"]
        assert "Ghibli" in result["prompt"]
        assert "pixel art" in result["prompt"]
