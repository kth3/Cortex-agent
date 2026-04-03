import pytest
from scripts.cortex.vector_engine import chunk_text

def test_chunk_text_empty():
    assert chunk_text("") == []
    assert chunk_text("   ") == []

def test_chunk_text_small():
    assert chunk_text("hello world", chunk_size=50) == ["hello world"]

def test_chunk_text_paragraphs_combined():
    text = "hello\n\nworld\n\n!"
    # With large chunk size, it combines them
    assert chunk_text(text, chunk_size=50) == ["hello\n\nworld\n\n!"]

def test_chunk_text_paragraphs_split():
    text = "paragraph 1\n\nparagraph 2\n\nparagraph 3"
    # chunk_size 15, "paragraph 1" is length 11. "paragraph 1\n\nparagraph 2" is length 24 > 15
    chunks = chunk_text(text, chunk_size=15, overlap=2)
    assert chunks == ["paragraph 1", "paragraph 2", "paragraph 3"]

def test_chunk_text_long_paragraph_split():
    text = "this is a very long paragraph that needs to be split"
    # Length of text is 52
    # chunk_size 20, overlap 5
    # "this is a very long " (20)
    # Next part starts at 20 - 5 = 15 -> "long paragraph that " (20)
    # Next part starts at 35 - 5 = 30 -> "that needs to be spl" (20)
    # Next part starts at 50 - 5 = 45 -> "e split" (7)
    chunks = chunk_text(text, chunk_size=20, overlap=5)

    assert len(chunks) > 1
    assert chunks[0] == "this is a very long "
    assert chunks[1] == "long paragraph that "
    assert chunks[2] == "that needs to be spl"
    assert chunks[3] == "e split"

    # Reconstruct to check everything is there (roughly)
    # just checking that the lengths are correct
    for chunk in chunks[:-1]:
        assert len(chunk) == 20
    assert len(chunks[-1]) <= 20

def test_chunk_text_trailing_whitespaces():
    text = "hello   \n\n   world   "
    assert chunk_text(text, chunk_size=5) == ["hello", "world"]
