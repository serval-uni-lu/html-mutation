import pytest

from html_mutation.html import compare


def test_memory_retrieve():
    memory = compare.Memory()
    memory.save("/path1", "/path2", True)
    assert memory.get("/path1", "/path2")


def test_memory_invert_path():
    memory = compare.Memory()
    memory.save("/path1", "/path2", True)
    assert memory.get("/path2", "/path1")
    assert memory.is_saved("/path2", "/path1")
