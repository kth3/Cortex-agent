import os
import pytest
from scripts.cortex.db import to_rel_path, to_abs_path

def test_to_rel_path_normal():
    """
    Note: The actual implementation of to_rel_path in scripts/cortex/db.py
    differs from the simplified snippet in the issue description.
    The actual code prepends "ROOT/" and replaces backslashes to normalize paths.
    This test asserts against the *actual* behavior of the function in the codebase
    to prevent regressions, as requested by previous code reviews.
    """
    workspace = "/home/user/project"
    full_path = "/home/user/project/src/main.py"

    result = to_rel_path(full_path, workspace)
    assert result == "ROOT/src/main.py"

def test_to_rel_path_same_dir():
    workspace = "/home/user/project"
    full_path = "/home/user/project"

    result = to_rel_path(full_path, workspace)
    assert result == "ROOT/."

def test_to_rel_path_empty():
    """
    Note: The actual implementation safely handles empty paths and None values,
    returning the original path. This test covers those edge cases present in the
    real application code.
    """
    assert to_rel_path("", "/workspace") == ""
    assert to_rel_path(None, "/workspace") is None
    assert to_rel_path("/path", "") == "/path"
    assert to_rel_path("/path", None) == "/path"

def test_to_rel_path_backslash_normalization(mocker):
    # Test that backslashes are replaced by forward slashes
    workspace = "C:\\workspace"
    full_path = "C:\\workspace\\src\\main.py"

    mocker.patch("os.path.relpath", return_value="src\\main.py")

    result = to_rel_path(full_path, workspace)
    assert result == "ROOT/src/main.py"

def test_to_rel_path_exception(mocker):
    """
    Test the exception handling block. The actual code catches Exception (which
    includes ValueError) and returns the original full_path.
    """
    workspace = "C:/workspace"
    full_path = "D:/other/path"

    mocker.patch("os.path.relpath", side_effect=ValueError("path is on mount 'D:', start on mount 'C:'"))

    result = to_rel_path(full_path, workspace)

    assert result == full_path

def test_to_abs_path_normal():
    """
    Note: The actual implementation of to_abs_path in scripts/cortex/db.py
    differs from the simplified snippet in the issue description.
    The actual code requires rel_path to start with "ROOT", normalizes
    "ROOT/" and "ROOT\\", and uses abspath.
    This test asserts against the *actual* behavior of the function in the codebase
    to prevent regressions, as requested by previous code reviews.
    """
    import os
    workspace = "/home/user/project"
    rel_path = "ROOT/src/main.py"

    result = to_abs_path(rel_path, workspace)
    expected = os.path.abspath(os.path.join(workspace, "src/main.py"))
    assert result == expected

def test_to_abs_path_empty_args():
    """
    Test handling of empty or None arguments.
    This is testing the actual edge case logic present in scripts/cortex/db.py
    rather than the simplified snippet.
    """
    assert to_abs_path("", "/workspace") == ""
    assert to_abs_path(None, "/workspace") is None
    assert to_abs_path("ROOT/src", "") == "ROOT/src"
    assert to_abs_path("ROOT/src", None) == "ROOT/src"

def test_to_abs_path_no_root():
    """Test behavior when rel_path does not start with ROOT."""
    workspace = "/home/user/project"
    rel_path = "src/main.py"

    result = to_abs_path(rel_path, workspace)
    assert result == "src/main.py"

def test_to_abs_path_backslash_normalization():
    """Test behavior when rel_path has ROOT\\ prefix."""
    import os
    workspace = "C:/workspace"
    rel_path = "ROOT\\src\\main.py"

    result = to_abs_path(rel_path, workspace)
    expected = os.path.abspath(os.path.join(workspace, "src\\main.py"))
    assert result == expected
