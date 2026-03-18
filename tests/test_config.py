import os

import pytest

from src.config import get_api_key


def test_valid_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    assert get_api_key() == "test-key-123"


def test_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(SystemExit, match="GEMINI_API_KEY is not set"):
        get_api_key()


def test_empty_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "   ")
    with pytest.raises(SystemExit, match="GEMINI_API_KEY is not set"):
        get_api_key()
