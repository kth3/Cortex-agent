from abc import ABC, abstractmethod
from pathlib import Path


class WorkspaceManager(ABC):
    """Abstract interface for managing isolated workspaces (e.g., Git Worktrees, Plastic Gluon)."""

    @abstractmethod
    def create_isolated_workspace(self, target_dir: Path, branch_or_changeset: str | None = None) -> bool:
        """
        Creates a new isolated workspace at the specified target directory.
        
        Args:
            target_dir: The directory where the isolated workspace should be created.
            branch_or_changeset: Optional branch, changeset, or commit to checkout.
            
        Returns:
            True if created successfully, False otherwise.
        """
        pass

    @abstractmethod
    def remove_isolated_workspace(self, target_dir: Path) -> bool:
        """
        Removes an isolated workspace from the specified target directory.
        
        Args:
            target_dir: The directory of the isolated workspace to remove.
            
        Returns:
            True if removed successfully, False otherwise.
        """
        pass

    @staticmethod
    def detect_vcs(workspace_root: Path) -> str | None:
        """
        Detects the Version Control System used in the given workspace root.
        
        Returns:
            'git', 'plastic', or None if neither is detected.
        """
        if (workspace_root / ".git").exists():
            return "git"
        if (workspace_root / ".plastic").exists():
            return "plastic"
        return None
