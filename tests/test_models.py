import json

from src.models import get_default_model, get_model_id, list_models


def _create_models_file(tmp_path):
    p = tmp_path / "models.json"
    data = {
        "flash": "gemini-2.5-flash-image",
        "pro": "gemini-3-pro-image-preview",
        "_default": "flash",
    }
    p.write_text(json.dumps(data))
    return p


def test_get_existing_alias(tmp_path):
    p = _create_models_file(tmp_path)
    assert get_model_id("flash", path=p) == "gemini-2.5-flash-image"


def test_get_missing_alias(tmp_path):
    p = _create_models_file(tmp_path)
    assert get_model_id("nonexistent", path=p) is None


def test_get_underscore_alias_rejected(tmp_path):
    p = _create_models_file(tmp_path)
    assert get_model_id("_default", path=p) is None


def test_list_models(tmp_path):
    p = _create_models_file(tmp_path)
    result = list_models(path=p)
    assert len(result) == 2
    aliases = [r[0] for r in result]
    assert "flash" in aliases
    assert "pro" in aliases


def test_list_models_default_marker(tmp_path):
    p = _create_models_file(tmp_path)
    result = list_models(path=p)
    for alias, model_id, is_default in result:
        if alias == "flash":
            assert is_default is True
        else:
            assert is_default is False


def test_get_default_model(tmp_path):
    p = _create_models_file(tmp_path)
    alias, model_id = get_default_model(path=p)
    assert alias == "flash"
    assert model_id == "gemini-2.5-flash-image"


def test_fallback_when_file_absent(tmp_path):
    p = tmp_path / "nonexistent.json"
    alias, model_id = get_default_model(path=p)
    assert alias == "flash"
    assert model_id == "gemini-2.5-flash-image"
