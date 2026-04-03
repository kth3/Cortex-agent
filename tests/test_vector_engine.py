import pytest
from scripts.cortex.vector_engine import chunk_text

def test_chunk_text_empty_or_whitespace():
    """Test with empty string and whitespace-only string."""
    assert chunk_text("") == []
    assert chunk_text("   \n  ") == []

def test_chunk_text_short_text():
    """Test with text shorter than the chunk size."""
    assert chunk_text("Hello world", chunk_size=50) == ["Hello world"]

def test_chunk_text_paragraphs_combine():
    """Test combining multiple short paragraphs until they reach chunk size."""
    text = "Para 1\n\nPara 2\n\nPara 3"
    # All paragraphs fit in one chunk (14 + 6 + 2 = 22 <= 30)
    assert chunk_text(text, chunk_size=30) == ["Para 1\n\nPara 2\n\nPara 3"]
    # First two fit in 15, third goes to next chunk
    assert chunk_text(text, chunk_size=15) == ["Para 1\n\nPara 2", "Para 3"]

def test_chunk_text_long_paragraph():
    """Test splitting a single long paragraph that exceeds chunk size."""
    text = "0123456789" * 3  # 30 chars
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    assert chunks == [
        "01234567890123456789",  # First 20 chars
        "567890123456789"        # Remaining 15 chars (with 5 chars overlap)
    ]

def test_chunk_text_mixed_paragraphs():
    """Test a mix of short paragraphs and long paragraphs that need splitting."""
    text = "Short para\n\n" + ("0123456789" * 3) + "\n\nAnother short"
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    assert chunks == [
        "Short para",
        "01234567890123456789",
        "567890123456789",
        "Another short"
    ]
