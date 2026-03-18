from pathlib import Path

from src.slugify import extract_keywords, slugify, strip_image_extension, unique_path


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


# --- extract_keywords tests (T003) ---


def test_extract_keywords_short_prompt():
    assert extract_keywords("un chat") == "chat"


def test_extract_keywords_long_prompt():
    result = extract_keywords("un magnifique paysage de montagne enneigée au coucher du soleil")
    words = result.split()
    assert len(words) <= 4


def test_extract_keywords_only_stop_words():
    assert extract_keywords("un le de la les des") == ""


def test_extract_keywords_mixed_fr_en():
    result = extract_keywords("a beautiful chat on the rooftop")
    words = result.split()
    assert len(words) <= 4
    assert "chat" in words
    assert "rooftop" in words
    # "a", "on", "the" are English stop words and should be filtered
    assert "a" not in words
    assert "on" not in words
    assert "the" not in words


def test_extract_keywords_one_two_words():
    assert extract_keywords("dragon") == "dragon"
    assert extract_keywords("red dragon") == "red dragon"


# --- strip_image_extension tests (T004) ---


def test_strip_image_extension_png():
    assert strip_image_extension("logo.png") == "logo"


def test_strip_image_extension_jpg():
    assert strip_image_extension("photo.jpg") == "photo"


def test_strip_image_extension_jpeg():
    assert strip_image_extension("image.jpeg") == "image"


def test_strip_image_extension_no_ext():
    assert strip_image_extension("my-file") == "my-file"


def test_strip_image_extension_non_image_ext():
    assert strip_image_extension("file.v2") == "file.v2"


def test_strip_image_extension_webp():
    assert strip_image_extension("photo.webp") == "photo"


# --- unique_path tests ---


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
