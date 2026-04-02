---
trigger: model_decision
---

# 인지 경제성 및 Zero-Hint 지침 (Cognitive Economy)

에이전트는 자신의 인지 부하(Token Bloat)를 상시 모니터링하며, 불필요한 '전역 힌트' 배제를 통해 추론의 정밀도를 유지해야 합니다.

## 1. Zero-Hint Architecture
- **최소 주입 원칙**: 최상위 규칙(`rule.md`)에는 불변의 철학만 남기고, 하위 규칙 파일에 대한 직접적인 링크나 상세 설명을 나열하지 않습니다.
- **On-Demand Intelligence**: 상세 프로토콜은 에이전트가 작업 중 이상 징후를 감지하거나 모호함을 느낄 때만 스스로 지식 저장소(Rules/DB)를 탐색하여 인지 영역으로 호출합니다.

## 2. 자율 탐색 프로토콜 (Autonomous Discovery)
- **탐색 트리거**: MCP 도구 에러, 사용자 정체성 모호성, 혹은 과거 작업 이력과의 불일치 발생 시 즉시 `pc_memory_search_knowledge`와 `list_dir`을 수행합니다.
- **인지 우선순위**: 
  1. 현재 작업 데이터 (코드, 로그)
  2. 명시적으로 호출된 규칙 파일 (`.agents/rules/`)
  3. DB 내 파편화된 메모리 (`patterns.md`, `memories` 등)

---

> [!TIP]
> 지능은 모든 것을 기억하는 것이 아니라, 필요할 때 정확한 답을 찾아내는 **'탐색의 경로'**를 설계하는 것입니다.
