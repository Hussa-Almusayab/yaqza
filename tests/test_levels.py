# pyright: reportMissingImports=false
import pytest

from engine.levels import LevelError, load_levels, validate_level


def test_levels_load_and_are_valid():
    levels = load_levels()
    assert len(levels) >= 2
    for level in levels:
        validate_level(level)


def test_bad_answer_index_is_rejected():
    bad = {"id": "x", "title": "t", "story": "s", "questions": [
        {"id": "q", "domain": "defense", "prompt": "p", "options": ["a", "b"],
         "answer": 5, "points": 10, "explain": "e"}]}
    with pytest.raises(LevelError):
        validate_level(bad)


def test_unknown_domain_is_rejected():
    bad = {"id": "x", "title": "t", "story": "s", "questions": [
        {"id": "q", "domain": "nope", "prompt": "p", "options": ["a", "b"],
         "answer": 0, "points": 10, "explain": "e"}]}
    with pytest.raises(LevelError):
        validate_level(bad)
