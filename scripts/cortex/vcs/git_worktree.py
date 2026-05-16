import logging
import subprocess
from pathlib import Path

from cortex.vcs.core import WorkspaceManager

logger = logging.getLogger(__name__)


class GitWorktreeManager(WorkspaceManager):
    def __init__(self, main_repo_path: Path):
        self.main_repo_path = main_repo_path

    def create_isolated_workspace(self, target_dir: Path, branch_or_changeset: str | None = None) -> bool:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        try:
            cmd = ["git", "worktree", "add"]
            if branch_or_changeset:
                cmd.extend(["-b", branch_or_changeset, str(target_dir)])
            else:
                # Default to detached HEAD based on current HEAD to prevent locking branches
                cmd.extend(["-d", str(target_dir)])

            subprocess.run(
                cmd,
                cwd=self.main_repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create git worktree: {e.stderr}")
            return False

    def remove_isolated_workspace(self, target_dir: Path) -> bool:
        try:
            subprocess.run(
                ["git", "worktree", "remove", "-f", str(target_dir)],
                cwd=self.main_repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to remove git worktree: {e.stderr}")
            return False
