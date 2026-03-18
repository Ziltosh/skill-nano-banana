from pathlib import Path

from src.slugify import slugify, unique_path


def test_basic_slugify():
    assert slugify("un chat") == "un-chat"


def test_unicode_slugify():
    assert slugify("café résumé") == "cafe-resume"


def test_special_chars():
    assert slugify("hello, world! @#$") == "hello-world"


def test_truncation():
    long_text = "a" * 100
    result = slugify(long_text, max_length=50)
    assert len(result) <= 50


def test_empty_string():
    assert slugify("") == "image"


def test_only_special_chars():
    assert slugify("@#$%^") == "image"


def test_trailing_hyphens_after_truncation():
    text = "hello-" + "a" * 50
    result = slugify(text, max_length=10)
    assert not result.endswith("-")


def test_unique_path_no_collision(tmp_path):
    path = unique_path(tmp_path, "test")
    assert path == tmp_path / "test.png"


def test_unique_path_with_collision(tmp_path):
    (tmp_path / "test.png").touch()
    path = unique_path(tmp_path, "test")
    assert path == tmp_path / "test-2.png"


def test_unique_path_multiple_collisions(tmp_path):
    (tmp_path / "test.png").touch()
    (tmp_path / "test-2.png").touch()
    path = unique_path(tmp_path, "test")
    assert path == tmp_path / "test-3.png"
