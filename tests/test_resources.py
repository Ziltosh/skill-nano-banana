import json

import pytest
from PIL import Image

from src.resources import list_tags, load_tag


def _create_tag(tmp_path, tag_name, num_images=2, meta_prompt=None):
    tag_dir = tmp_path / tag_name
    tag_dir.mkdir()
    for i in range(num_images):
        img = Image.new("RGB", (10, 10), color="red")
        img.save(tag_dir / f"img{i}.png")
    if meta_prompt is not None:
        (tag_dir / "meta.json").write_text(json.dumps({"prompt": meta_prompt}))
    return tag_dir


def test_list_tags(tmp_path):
    _create_tag(tmp_path, "face-kim")
    _create_tag(tmp_path, "landscape")
    assert list_tags(resources_dir=tmp_path) == ["face-kim", "landscape"]


def test_list_tags_empty(tmp_path):
    assert list_tags(resources_dir=tmp_path) == []


def test_list_tags_ignores_dotfiles(tmp_path):
    (tmp_path / ".hidden").mkdir()
    _create_tag(tmp_path, "visible")
    assert list_tags(resources_dir=tmp_path) == ["visible"]


def test_load_images(tmp_path):
    _create_tag(tmp_path, "test-tag", num_images=3)
    images, prompt = load_tag("test-tag", resources_dir=tmp_path)
    assert len(images) == 3
    assert all(p.suffix == ".png" for p in images)
    assert prompt is None


def test_load_with_meta(tmp_path):
    _create_tag(tmp_path, "face-kim", meta_prompt="this person must appear")
    images, prompt = load_tag("face-kim", resources_dir=tmp_path)
    assert len(images) == 2
    assert prompt == "this person must appear"


def test_missing_tag(tmp_path):
    with pytest.raises(ValueError, match="not found"):
        load_tag("nonexistent", resources_dir=tmp_path)


def test_empty_tag(tmp_path):
    (tmp_path / "empty-tag").mkdir()
    with pytest.raises(ValueError, match="no images"):
        load_tag("empty-tag", resources_dir=tmp_path)


def test_filters_non_image_files(tmp_path):
    tag_dir = tmp_path / "mixed"
    tag_dir.mkdir()
    Image.new("RGB", (10, 10)).save(tag_dir / "valid.png")
    (tag_dir / "readme.txt").write_text("not an image")
    (tag_dir / "data.json").write_text("{}")
    images, _ = load_tag("mixed", resources_dir=tmp_path)
    assert len(images) == 1
    assert images[0].name == "valid.png"


def test_supports_jpg_webp(tmp_path):
    tag_dir = tmp_path / "formats"
    tag_dir.mkdir()
    Image.new("RGB", (10, 10)).save(tag_dir / "a.png")
    Image.new("RGB", (10, 10)).save(tag_dir / "b.jpg")
    Image.new("RGB", (10, 10)).save(tag_dir / "c.webp")
    images, _ = load_tag("formats", resources_dir=tmp_path)
    assert len(images) == 3
