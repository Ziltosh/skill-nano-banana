"""Tests for CLI argument validation."""

import pytest

from src.generate import parse_args


def test_valid_args_with_all_flags():
    args = parse_args(["a castle", "--style", "ghibli", "--model", "pro", "--include", "face-kim"])
    assert args.prompt == "a castle"
    assert args.style == "ghibli"
    assert args.model == "pro"
    assert args.include == ["face-kim"]


def test_valid_args_prompt_only():
    args = parse_args(["a cat"])
    assert args.prompt == "a cat"
    assert args.style is None
    assert args.model is None
    assert args.include == []


def test_multiple_include():
    args = parse_args(["test", "--include", "face-kim", "--include", "bg-forest"])
    assert args.include == ["face-kim", "bg-forest"]


def test_flags_in_any_order():
    args = parse_args(["test", "--model", "pro", "--style", "ghibli", "--include", "tag1"])
    assert args.model == "pro"
    assert args.style == "ghibli"
    assert args.include == ["tag1"]


def test_unknown_flag_raises():
    with pytest.raises(SystemExit):
        parse_args(["test", "--unknown-flag"])


def test_missing_style_value_raises():
    with pytest.raises(SystemExit):
        parse_args(["test", "--style"])


def test_missing_model_value_raises():
    with pytest.raises(SystemExit):
        parse_args(["test", "--model"])


def test_missing_prompt_raises():
    with pytest.raises(SystemExit):
        parse_args([])
