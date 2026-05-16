import logging
import shutil
import subprocess
from pathlib import Path

from cortex.vcs.core import WorkspaceManager

logger = logging.getLogger(__name__)


class PlasticWorkspaceManager(WorkspaceManager):
    def __init__(self, main_repo_path: Path):
        self.main_repo_path = main_repo_path

    def create_isolated_workspace(self, target_dir: Path, branch_or_changeset: str | None = None) -> bool:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        ws_name = f"cortex_iso_{target_dir.name}"
        try:
            # In Plastic SCM, cm mkworkspace creates a new workspace.
            # We ideally want a Partial workspace (Gluon) pointing to the same repo.
            # Due to CLI complexity, we create a standard workspace here.
            subprocess.run(
                ["cm", "mkworkspace", ws_name, str(target_dir)],
                cwd=self.main_repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create plastic workspace: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            return False

    def remove_isolated_workspace(self, target_dir: Path) -> bool:
        ws_name = f"cortex_iso_{target_dir.name}"
        try:
            subprocess.run(
                ["cm", "rmworkspace", ws_name],
                cwd=self.main_repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to remove plastic workspace: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            return False
