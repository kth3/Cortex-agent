"""
영구 지식 저장소 관리자 (PersistentMemoryManager)
- db.py의 memories 테이블(FTS5 포함)을 사용
- agent-memory-mcp 흡수 통합 버전
"""
import time
import json
from cortex.db import get_connection, init_schema


class PersistentMemoryManager:
    def __init__(self, workspace: str):
        self.workspace = workspace
        # 스키마 보장
        conn = get_connection(workspace)
        try:
            init_schema(conn)
        finally:
            conn.close()

    def write(self, project_id: str, data: dict) -> bool:
        """
        영구 지식 저장 또는 갱신
        data: {key, category, content, tags=[], relationships={}}
        """
        key = data.get("key", "")
        if not key:
            return False

        conn = get_connection(self.workspace)
        try:
            now = int(time.time())
            tags_json = json.dumps(data.get("tags") or [], ensure_ascii=False)
            rel_json = json.dumps(data.get("relationships") or {}, ensure_ascii=False)

            existing = conn.execute(
                "SELECT key FROM memories WHERE key = ?", (key,)
            ).fetchone()

            if existing:
                conn.execute(
                    """UPDATE memories
                       SET category=?, content=?, tags=?, relationships=?, updated_at=?,
                           access_count=access_count+1
                       WHERE key=?""",
                    (
                        data.get("category", "general"),
                        data.get("content", ""),
                        tags_json,
                        rel_json,
                        now,
                        key,
                    ),
                )
            else:
                conn.execute(
                    """INSERT INTO memories
                       (key, project_id, category, content, tags, relationships, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        key,
                        project_id,
                        data.get("category", "general"),
                        data.get("content", ""),
                        tags_json,
                        rel_json,
                        now,
                        now,
                    ),
                )
            conn.commit()
            return True
        except Exception as e:
            print(f"[persistent_memory] write error: {e}")
            return False
        finally:
            conn.close()

    def read(self, project_id: str, key: str) -> dict:
        """키로 단일 메모리 조회"""
        conn = get_connection(self.workspace)
        try:
            row = conn.execute(
                "SELECT * FROM memories WHERE key = ?", (key,)
            ).fetchone()
            if row:
                conn.execute(
                    "UPDATE memories SET access_count=access_count+1 WHERE key=?", (key,)
                )
                conn.commit()
                d = dict(row)
                d["tags"] = json.loads(d.get("tags") or "[]")
                d["relationships"] = json.loads(d.get("relationships") or "{}")
                return d
            return {"error": f"Key '{key}' not found"}
        finally:
            conn.close()

    def search(self, project_id: str, query: str, category: str = None, limit: int = 10) -> list:
        """FTS5 전문 검색"""
        conn = get_connection(self.workspace)
        try:
            safe_query = f'"{query.replace(chr(34), chr(34)+chr(34))}"'
            if category:
                rows = conn.execute(
                    """SELECT m.* FROM memories_fts f
                       JOIN memories m ON m.rowid = f.rowid
                       WHERE memories_fts MATCH ? AND m.category = ?
                       ORDER BY rank LIMIT ?""",
                    (safe_query, category, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT m.* FROM memories_fts f
                       JOIN memories m ON m.rowid = f.rowid
                       WHERE memories_fts MATCH ?
                       ORDER BY rank LIMIT ?""",
                    (safe_query, limit),
                ).fetchall()

            results = []
            for row in rows:
                d = dict(row)
                d["tags"] = json.loads(d.get("tags") or "[]")
                d["relationships"] = json.loads(d.get("relationships") or "{}")
                results.append(d)
            return results
        except Exception:
            # FTS 실패 시 LIKE 폴백
            try:
                rows = conn.execute(
                    "SELECT * FROM memories WHERE content LIKE ? ORDER BY updated_at DESC LIMIT ?",
                    (f"%{query}%", limit),
                ).fetchall()
                return [dict(r) for r in rows]
            except Exception as e2:
                return [{"error": str(e2)}]
        finally:
            conn.close()

    def delete_many(self, project_id: str, keys: list) -> int:
        """주어진 key 리스트에 해당하는 메모리 레코드를 영구 삭제 (FTS 동기화 포함)"""
        if not keys:
            return 0
        conn = get_connection(self.workspace)
        try:
            placeholders = ",".join(["?"] * len(keys))
            cursor = conn.execute(f"DELETE FROM memories WHERE key IN ({placeholders})", keys)
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        except Exception as e:
            print(f"[persistent_memory] delete error: {e}")
            return 0
        finally:
            conn.close()

    def get_stats(self, project_id: str) -> dict:
        """메모리 저장소 통계"""
        conn = get_connection(self.workspace)
        try:
            total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            by_cat = conn.execute(
                "SELECT category, COUNT(*) as cnt FROM memories GROUP BY category"
            ).fetchall()
            return {
                "total_memories": total,
                "by_category": {r["category"]: r["cnt"] for r in by_cat},
            }
        finally:
            conn.close()
