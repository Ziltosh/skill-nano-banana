import json

from src.styles import add_style, get_style, list_styles


def _create_styles_file(tmp_path):
    p = tmp_path / "styles.json"
    data = {"ghibli": "ghibli style text", "pixel-art": "pixel art text"}
    p.write_text(json.dumps(data))
    return p


def test_get_existing_style(tmp_path):
    p = _create_styles_file(tmp_path)
    assert get_style("ghibli", path=p) == "ghibli style text"


def test_get_missing_style(tmp_path):
    p = _create_styles_file(tmp_path)
    assert get_style("nonexistent", path=p) is None


def test_list_styles(tmp_path):
    p = _create_styles_file(tmp_path)
    assert list_styles(path=p) == ["ghibli", "pixel-art"]


def test_list_styles_empty(tmp_path):
    p = tmp_path / "styles.json"
    assert list_styles(path=p) == []


def test_add_new_style(tmp_path):
    p = _create_styles_file(tmp_path)
    success, action = add_style("watercolor", "watercolor text", path=p)
    assert success is True
    assert action == "created"
    assert get_style("watercolor", path=p) == "watercolor text"


def test_add_existing_style_no_force(tmp_path):
    p = _create_styles_file(tmp_path)
    success, action = add_style("ghibli", "new text", path=p)
    assert success is False
    assert action == "exists"
    assert get_style("ghibli", path=p) == "ghibli style text"


def test_add_existing_style_with_force(tmp_path):
    p = _create_styles_file(tmp_path)
    success, action = add_style("ghibli", "new text", force=True, path=p)
    assert success is True
    assert action == "replaced"
    assert get_style("ghibli", path=p) == "new text"
