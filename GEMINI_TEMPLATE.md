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
- **보고 의무**: 작업 보고는 모든 분석 및 답변이 끝난 **최종 응답의 최하단에 딱 한 번**만 기재한다. (중간 과정 생략)
- **Skill 표기 원칙**: `pc_` 도구를 통한 검색 결과로 참조된 모든 스킬 ID를 쉼표로 구분하여 명시한다. **식별자 외의 부연 설명(예: "(참조됨)")은 절대 붙이지 않는다.** (예: `Skill: frontend-security-coder, clarity-gate`)
- **MCP 표기 원칙**: 성공적으로 호출된 MCP 서버 명칭만 명시한다. (예: `MCP: cortex-mcp`)
