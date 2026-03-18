"""Tests for create_style script."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.create_style import create_style, parse_args


class TestParseArgs:
    def test_name_and_description(self):
        args = parse_args(["cyberpunk", "neon lights and dark"])
        assert args.name == "cyberpunk"
        assert args.description == "neon lights and dark"
        assert args.force is False

    def test_with_force(self):
        args = parse_args(["cyberpunk", "neon lights", "--force"])
        assert args.force is True

    def test_missing_args(self):
        with pytest.raises(SystemExit):
            parse_args([])

    def test_missing_description(self):
        with pytest.raises(SystemExit):
            parse_args(["cyberpunk"])


class TestCreateStyle:
    def test_create_new(self, tmp_path):
        styles_file = tmp_path / "styles.json"
        styles_file.write_text("{}")

        result = create_style("my-style", "cool style", styles_file=styles_file)

        assert result["success"] is True
        assert result["action"] == "created"
        assert result["name"] == "my-style"

        data = json.loads(styles_file.read_text())
        assert data["my-style"] == "cool style"

    def test_conflict_no_force(self, tmp_path):
        styles_file = tmp_path / "styles.json"
        styles_file.write_text(json.dumps({"ghibli": "existing"}))

        result = create_style("ghibli", "new text", styles_file=styles_file)

        assert result["success"] is False
        assert result["code"] == "STYLE_EXISTS"
        assert "existing" in result["existing_prompt"]

    def test_replace_with_force(self, tmp_path):
        styles_file = tmp_path / "styles.json"
        styles_file.write_text(json.dumps({"ghibli": "old text"}))

        result = create_style(
            "ghibli", "new text", force=True, styles_file=styles_file
        )

        assert result["success"] is True
        assert result["action"] == "replaced"

        data = json.loads(styles_file.read_text())
        assert data["ghibli"] == "new text"

    def test_invalid_name(self, tmp_path):
        styles_file = tmp_path / "styles.json"
        styles_file.write_text("{}")

        result = create_style("Invalid Name!", "text", styles_file=styles_file)

        assert result["success"] is False
        assert "kebab-case" in result["error"]
