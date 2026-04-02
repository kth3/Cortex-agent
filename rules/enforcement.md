---
trigger: glob
globs: **/*.{java,py,js,jsx,ts,tsx,html,css,json,md,yml,yaml,xml,sql,sh,gradle,properties}

---

# 지식 탐색 강제화 지침 (Mandatory Discovery)

에이전트가 프로젝트의 주요 소스 코드를 분석하거나 수정할 때, 자신의 일반적인 LLM 지식에 의존하는 것을 금기시하며 반드시 프로젝트 고유의 지식 자산(Skill/Pattern)을 먼저 탐색해야 합니다.

## 1. 탐색 의무 (The Search Duty)
- **분석 전 필수 단계**: 코드의 기능이나 구조를 분석하기 전, 반드시 하단의 MCP 도구 중 하나 이상을 사용하여 관련 스킬을 조회해야 합니다.
  - `pc_memory_search_knowledge`: 관련 로직이나 패턴 검색
  - `pc_capsule`: 파일 간의 맥락적 관계 파악
  - `pc_memory_sync_skills`: 필요한 전문가 스킬이 있는지 확인

## 2. 노 스킬(No-Skill) 현상 방지
- 작업 종료 시 `Skill` 항목이 `none`으로 표기되거나, DB에 존재하지 않는 임의의 추상적 태그를 사용하는 것을 "인지적 게으름"으로 간주합니다.
- 반드시 `pc_memory_search_knowledge` 등을 통해 조회된 **실제 지식 자산(Asset)의 식별자**를 사용하십시오.
- 1,200여 개의 미세 스킬 중 단 하나라도 이번 작업과 연관된 것이 없는지 철저히 검증하고, 만약 없다면 **새로운 성공 패턴(`success_pattern`)으로 인지 자산화**할 것을 검토하십시오.

## 3. 예외 상황
- 오직 1줄 이하의 단순 타이포 수정이나, 인프라 수복(`Maintenance-First`) 도중의 긴급 정비 상황에서만 탐색을 생략할 수 있습니다.

---

> [!CAUTION]
> 분석 결과에 프로젝트 고유의 컨벤션이나 기존 패턴이 반영되지 않았을 경우, 이는 **인프라 결함**과 동일한 수준의 실패로 간주됩니다.