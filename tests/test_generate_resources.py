"""Tests for resource inclusion in generate_image."""

import json
from unittest.mock import MagicMock, patch

from PIL import Image

from src.generate import generate_image


def _create_tag(tmp_path, tag_name, num_images=2, meta_prompt=None):
    res_dir = tmp_path / "resources"
    tag_dir = res_dir / tag_name
    tag_dir.mkdir(parents=True, exist_ok=True)
    for i in range(num_images):
        Image.new("RGB", (10, 10), color="red").save(tag_dir / f"img{i}.png")
    if meta_prompt:
        (tag_dir / "meta.json").write_text(json.dumps({"prompt": meta_prompt}))
    return res_dir


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
def test_include_loads_images(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "face-kim", num_images=2)
    mock_client = _mock_success(mock_genai)

    result = generate_image(
        prompt="portrait",
        api_key="key",
        include_tags=["face-kim"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    call_args = mock_client.models.generate_content.call_args
    contents = call_args.kwargs["contents"]
    # 2 images + 1 prompt text
    image_count = sum(1 for c in contents if isinstance(c, Image.Image))
    assert image_count == 2


@patch("src.generate.genai")
def test_include_enriches_prompt_with_meta(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "face-kim", meta_prompt="this person must appear")
    _mock_success(mock_genai)

    result = generate_image(
        prompt="portrait",
        api_key="key",
        include_tags=["face-kim"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert "this person must appear" in result["prompt"]


@patch("src.generate.genai")
def test_include_without_meta_sends_images_only(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "landscape", num_images=1)
    _mock_success(mock_genai)

    result = generate_image(
        prompt="a view",
        api_key="key",
        include_tags=["landscape"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert result["prompt"] == "a view"  # no meta enrichment


@patch("src.generate.genai")
def test_unknown_tag_error(mock_genai, tmp_path):
    res_dir = tmp_path / "resources"
    res_dir.mkdir()

    result = generate_image(
        prompt="test",
        api_key="key",
        include_tags=["nonexistent"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is False
    assert result["code"] == "UNKNOWN_TAG"


@patch("src.generate.genai")
def test_empty_tag_error(mock_genai, tmp_path):
    res_dir = tmp_path / "resources"
    (res_dir / "empty-tag").mkdir(parents=True)

    result = generate_image(
        prompt="test",
        api_key="key",
        include_tags=["empty-tag"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is False
    assert result["code"] == "EMPTY_RESOURCES"


@patch("src.generate.genai")
def test_multiple_include_combines(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "tag1", num_images=1)
    _create_tag(tmp_path, "tag2", num_images=2)
    mock_client = _mock_success(mock_genai)

    result = generate_image(
        prompt="test",
        api_key="key",
        include_tags=["tag1", "tag2"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    call_args = mock_client.models.generate_content.call_args
    contents = call_args.kwargs["contents"]
    image_count = sum(1 for c in contents if isinstance(c, Image.Image))
    assert image_count == 3  # 1 + 2


@patch("src.generate.genai")
def test_include_plus_images_combines(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "tag1", num_images=1)
    chat_img = tmp_path / "chat.png"
    Image.new("RGB", (10, 10)).save(chat_img)
    mock_client = _mock_success(mock_genai)

    result = generate_image(
        prompt="test",
        api_key="key",
        include_tags=["tag1"],
        image_paths=[str(chat_img)],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    call_args = mock_client.models.generate_content.call_args
    contents = call_args.kwargs["contents"]
    image_count = sum(1 for c in contents if isinstance(c, Image.Image))
    assert image_count == 2  # 1 resource + 1 chat


@patch("src.generate.genai")
def test_include_plus_style_cumulates(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "face-kim", meta_prompt="person must appear")
    styles_file = tmp_path / "styles.json"
    styles_file.write_text(json.dumps({"ghibli": "Ghibli style"}))
    _mock_success(mock_genai)

    result = generate_image(
        prompt="portrait",
        api_key="key",
        include_tags=["face-kim"],
        style=["ghibli"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        styles_file=styles_file,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    assert "person must appear" in result["prompt"]
    assert "Ghibli style" in result["prompt"]


@patch("src.generate.genai")
def test_text_combined_with_include(mock_genai, tmp_path):
    res_dir = _create_tag(tmp_path, "face-kim", meta_prompt="person must appear")
    _mock_success(mock_genai)

    result = generate_image(
        prompt="portrait",
        api_key="key",
        text="HELLO",
        include_tags=["face-kim"],
        output_dir=tmp_path / "out",
        resources_dir=res_dir,
        history_file=tmp_path / "history.jsonl",
    )

    assert result["success"] is True
    prompt = result["prompt"]
    # Text instruction should be present
    assert "HELLO" in prompt
    # Resource prompt should be present
    assert "person must appear" in prompt
    # Text instruction should come before resource prompt
    text_pos = prompt.index("HELLO")
    resource_pos = prompt.index("person must appear")
    assert text_pos < resource_pos
