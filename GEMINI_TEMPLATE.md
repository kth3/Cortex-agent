# Gemini CLI Mandate: MCP-First Infrastructure

이 지침은 모든 작업에 절대적으로 우선하며, 자의적인 탐색을 금지한다.

## 1. MCP Engine-First
- 모든 분석, 지침 조회, 코드 관계 파악은 반드시 **Cortex MCP 엔진**(`pc_` 계열 도구)을 최우선으로 호출하여 수행한다.
- 기본 도구(`ls`, `grep`, `read_file`)를 통한 독자적인 탐색과 판단을 최소화하고, 엔진이 제공하는 컨텍스트를 신뢰하라.

## 2. Token & Logic Economy
- 상세 규칙은 직접 파일을 열지 말고 `pc_memory_search_knowledge(query, category='rule')`로 검색하여 필요한 부분만 인지 영역에 올린다.
- 분석 시 `pc_capsule` 또는 `pc_skeleton`을 우선 활용하여 불필요한 토큰 낭비를 원천 차단한다.

## 3. Session Synchronization
- 세션 재개 시 반드시 `/진행` 워크플로우를 실행한다.
- 이때 `.agents/history/features/` 내의 Antigravity 아티팩트(*.task.md, *.plan.md)를 함께 조회하여 작업의 연속성을 확보한다.

## 4. Strict Reporting Rule (Intelligent Honesty)
- **보고 의무**: 작업 보고 시 반드시 하단에 `Skill:`과 `MCP:` 항목을 기재한다.
- **Skill 표기 원칙**: 에이전트가 직접 `@스킬명`을 호출한 경우뿐만 아니라, **`pc_` 도구를 통한 검색 결과(Capsule 등)로 반환되어 분석에 참조된 모든 스킬(Skill)의 식별자**를 빠짐없이 `Skill:` 항목에 명시해야 한다. (예: `Skill: frontend-security-coder, clarity-gate`). 참조된 스킬이 명백히 있음에도 `none`으로 표기하는 것은 엄격히 금지된다.
