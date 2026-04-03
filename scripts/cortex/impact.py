"""
영향 분석(Impact Analysis) 및 논리 흐름(Logic Flow) 추적 모듈.
"""
from collections import deque

def get_impact_tree(conn, node_id, direction='both', max_depth=3):
    """
    특정 노드로부터의 영향도 트리 생성 (BFS)
    - direction: 'callers' (나를 호출하는 곳), 'callees' (내가 호출하는 곳), 'both'
    """
    impact_graph = {"nodes": {}, "edges": []}
    queue = deque([(node_id, 0)])
    visited = {node_id}
    
    # 루트 노드 추가
    root = conn.execute("SELECT id, fqn, type, file_path FROM nodes WHERE id = ?", (node_id,)).fetchone()
    if not root: return impact_graph
    impact_graph["nodes"][node_id] = dict(root)

    while queue:
        curr_id, depth = queue.popleft()
        if depth >= max_depth: continue

        # Callees (내가 호출하는 노드들)
        if direction in ['callees', 'both']:
            callees = conn.execute(\
                "SELECT n.id, n.fqn, n.type, n.file_path FROM edges e JOIN nodes n ON e.target_id = n.id WHERE e.source_id = ?", \
                (curr_id,)).fetchall()
            for c in callees:
                c_dict = dict(c)
                cid = c_dict["id"]
                impact_graph["edges"].append({"from": curr_id, "to": cid, "type": "calls"})
                if cid not in visited:
                    visited.add(cid)
                    impact_graph["nodes"][cid] = c_dict
                    queue.append((cid, depth + 1))

        # Callers (나를 호출하는 노드들)
        if direction in ['callers', 'both']:
            callers = conn.execute(\
                "SELECT n.id, n.fqn, n.type, n.file_path FROM edges e JOIN nodes n ON e.source_id = n.id WHERE e.target_id = ?", \
                (curr_id,)).fetchall()
            for c in callers:
                c_dict = dict(c)
                cid = c_dict["id"]
                impact_graph["edges"].append({"from": cid, "to": curr_id, "type": "calls"})
                if cid not in visited:
                    visited.add(cid)
                    impact_graph["nodes"][cid] = c_dict
                    queue.append((cid, depth + 1))

    return impact_graph

def find_logic_flow(conn, from_fqn, to_fqn):
    """
    두 구체적인 기호 사이의 실행 경로 탐색 (DFS/Dijkstra)
    """
    start_node = conn.execute("SELECT id FROM nodes WHERE fqn = ?", (from_fqn,)).fetchone()
    end_node = conn.execute("SELECT id FROM nodes WHERE fqn = ?", (to_fqn,)).fetchone()
    if not start_node or not end_node:
        return {"error": "Start or End node not found"}
        
    sid, eid = start_node[0], end_node[0]
    
    # 간단한 BFS 경로 탐색
    queue = deque([[sid]])
    visited = {sid}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == eid:
            # 경로 상세 정보로 변환 (IN 절을 사용해 N+1 문제 해결)
            if not path:
                return []

            node_map = {}
            chunk_size = 900

            for i in range(0, len(path), chunk_size):
                chunk = path[i:i + chunk_size]
                placeholders = ','.join(['?'] * len(chunk))
                query = f"SELECT id, fqn, file_path, start_line FROM nodes WHERE id IN ({placeholders})"
                rows = conn.execute(query, tuple(chunk)).fetchall()
                for row in rows:
                    node_map[row['id']] = dict(row)

            flow = []
            for nid in path:
                if nid in node_map:
                    ninfo = node_map[nid]
                    # 원래 반환하던 키들만 추출
                    flow.append({
                        'fqn': ninfo['fqn'],
                        'file_path': ninfo['file_path'],
                        'start_line': ninfo['start_line']
                    })
            return flow
            
        callees = conn.execute("SELECT to_id FROM edges WHERE from_id = ?", (node,)).fetchall()
        for c in callees:
            cid = c[0]
            if cid not in visited:
                visited.add(cid)
                new_path = list(path)
                new_path.append(cid)
                queue.append(new_path)
    
    return {"error": "No path found between symbols"}
