import re
import os

def parse_markdown_file(content: str, file_path: str) -> list:
    """
    마크다운 파일(특히 스킬 문서)의 메타데이터와 본문을 단일 DB 노드로 변환합니다.
    """
    nodes = []
    
    # 기본값 설정
    skill_name = ""
    description = ""
    start_line = 1
    end_line = content.count('\n') + 1

    # 경로에서 스킬 이름 유추 (예: .../skills/my-skill/SKILL.md -> my-skill)
    # 부모 디렉토리 이름 사용 우선
    parts = file_path.replace('\\', '/').split('/')
    if len(parts) >= 2 and (parts[-1] == 'SKILL.md' or parts[-1] == 'README.md'):
        skill_name = parts[-2]
    else:
        skill_name = os.path.splitext(os.path.basename(file_path))[0]

    # Frontmatter 파싱 (--- ... ---)
    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            fm_block = content[3:end_idx].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    k = k.strip().lower()
                    v = v.strip().strip('"').strip("'")
                    if k == "name":
                        skill_name = v
                    elif k == "description":
                        description = v
    
    # docstring이 비어있으면 첫 번째 본문 단락에서 추출
    if not description:
        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL).strip()
        first_para = body.split("\n\n")[0].replace("#", "").strip()
        description = first_para[:200]

    # FQN 생성
    fqn = f"skill:{skill_name}"
    
    # 노드 고유 ID (파일 경로 기반으로 해시)
    import hashlib
    node_id = hashlib.md5(file_path.encode('utf-8')).hexdigest()
    
    # 단일 노드 반환
    node = {
        "id": node_id,
        "type": "skill",
        "name": skill_name,
        "fqn": fqn,
        "file_path": file_path,
        "start_line": start_line,
        "end_line": end_line,
        "signature": "",
        "return_type": "",
        "docstring": description,
        "is_exported": 1,
        "is_async": 0,
        "is_test": 0,
        "raw_body": content,
        "skeleton_standard": "",
        "skeleton_minimal": "",
        "language": "markdown",
    }
    nodes.append(node)
    
    return {"nodes": nodes, "edges": []}
