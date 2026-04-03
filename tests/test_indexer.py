import pytest
from scripts.cortex.indexer import compute_hash

def test_compute_hash_deterministic():
    """Test that the same input produces the same hash"""
    content = "print('hello world')"
    assert compute_hash(content) == compute_hash(content)

def test_compute_hash_empty():
    """Test hashing an empty string"""
    result = compute_hash("")
    assert isinstance(result, str)
    assert len(result) == 32  # blake2b with digest_size=16 gives 32 hex chars

def test_compute_hash_length():
    """Test the output length is consistently 32 characters"""
    result1 = compute_hash("a")
    result2 = compute_hash("a" * 1000)
    assert len(result1) == 32
    assert len(result2) == 32

def test_compute_hash_different_inputs():
    """Test that different inputs produce different hashes"""
    hash1 = compute_hash("hello")
    hash2 = compute_hash("world")
    assert hash1 != hash2

def test_compute_hash_unicode():
    """Test hashing strings with unicode characters"""
    content_korean = "안녕하세요"
    content_emoji = "👋 🌎"

    hash1 = compute_hash(content_korean)
    hash2 = compute_hash(content_emoji)

    assert isinstance(hash1, str)
    assert isinstance(hash2, str)
    assert len(hash1) == 32
    assert len(hash2) == 32
    assert hash1 != hash2

def test_compute_hash_known_output():
    """Test against a known output for the current algorithm (blake2b digest_size=16)"""
    # The current codebase uses: hashlib.blake2b(content.encode("utf-8"), digest_size=16).hexdigest()
    # "hello" should hash to 46fb7408d4f285228f4af516ea25851b
    # This also checks that errors='replace' or similar isn't breaking basic utf-8
    assert compute_hash("hello") == "46fb7408d4f285228f4af516ea25851b"
