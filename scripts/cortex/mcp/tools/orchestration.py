"""MCP tool handler module.

- 책임: 클라이언트로부터 전달된 MCP 요청 인자를 검증하고, 도메인 함수를 호출한 뒤 응답을 포맷팅하는 책임을 가진다.
- 주의: 외부 클라이언트와의 통신 계약을 담당하므로, tool 이름, 반환 구조, error response 형식을 임의로 변경하지 않는다.
"""
import sys
from pathlib import Path

# 경로 설정
SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from cortex.orchestration import manage_todo, create_contract
from cortex.memories import working as pc_mem_mod
from cortex.hooks import manager as pc_hooks

CONTRACT_OBSERVATION_CATEGORY = "decision"
AFTER_SAVE_OBSERVATION_HOOK = "after_save_observation"


def _contract_observation_message(contract_id: str) -> str:
    return f"Contract created: {contract_id}"


def _save_contract_observation(ctx, contract_id: str, contract_path: str) -> None:
    pc_mem_mod.save_observation(
        ctx.workspace,
        ctx.session_id,
        CONTRACT_OBSERVATION_CATEGORY,
        _contract_observation_message(contract_id),
        [contract_path],
    )
    pc_hooks.dispatch(ctx.workspace, AFTER_SAVE_OBSERVATION_HOOK)


def call_todo_manager(ctx, args):
    """manages todo list"""
    return manage_todo(
        ctx.workspace, args["action"], args.get("task"), args.get("task_id")
    )


def call_create_contract(ctx, args):
    """creates a contract for a task"""
    lane_id = args["lane_id"]
    files_to_modify = args.get("files_to_modify") or []
    
    # Phase 3: Collision Detection
    import relay
    relay.update_files_to_modify(lane_id, files_to_modify)
    
    if files_to_modify:
        active_files = set(relay.get_active_files(exclude_lane_id=lane_id))
        requested_files = set(files_to_modify)
        if requested_files.intersection(active_files):
            # Phase 4: Dynamic Redirection
            from cortex.paths import resolve_workspace, workspace_key
            from cortex.vcs.core import WorkspaceManager
            from cortex.vcs.git_worktree import GitWorktreeManager
            from cortex.vcs.plastic_workspace import PlasticWorkspaceManager
            
            main_repo = resolve_workspace(ctx.workspace)
            vcs_type = WorkspaceManager.detect_vcs(main_repo)
            
            if vcs_type:
                target_dir = main_repo / ".cortex" / "isolated_workspaces" / workspace_key(main_repo) / lane_id
                
                if not target_dir.exists():
                    wm = GitWorktreeManager(main_repo) if vcs_type == "git" else PlasticWorkspaceManager(main_repo)
                    success = wm.create_isolated_workspace(target_dir)
                    if success:
                        relay.set_isolated_workspace(lane_id, str(main_repo), str(target_dir))
                        ctx.workspace = str(target_dir)
                        args["instructions"] = args.get("instructions", "") + f"\n\n[SYSTEM] A file collision was detected. You have been isolated into a {vcs_type} workspace at {target_dir}. Continue normally."

    res = create_contract(
        ctx.workspace,
        ctx.session_id,
        args["lane_id"],
        args["task_name"],
        args["instructions"],
        args.get("files_to_modify"),
    )
    _save_contract_observation(ctx, res["contract_id"], res["path"])
    return res
