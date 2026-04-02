---
name: jules
description: Google Jules AI를 사용하여 심층 코드 리뷰를 수행합니다.
---

이 워크플로우는 Local MCP 서버 도구를 사용하여 Jules AI API를 호출하고 현재 코드베이스의 품질을 정밀 진단합니다.

## 실행 단계
1. **프로젝트 컨텍스트 추출**: 로컬 MCP 도구 `jules_request_review`를 호출할 때 지침(instructions)에 프로젝트 ADR 및 규칙 컨텍스트를 포함합니다.
2. **리뷰 요청**: 
    - **도구 호출**: `mcp_local_server`의 `jules_request_review`를 사용합니다.
    - **인자**: `commit_id`, `diff_content`, `instructions`를 전달합니다.
3. **분석 확인**: 요청 성공 후 사용자는 Jules AI 웹사이트에서 직접 분석 결과를 확인합니다.

## 사용법
- `/jules`: 전체 변경 사항에 대해 리뷰를 요청합니다.
- `@jules_api.py` (API 연동 스크립트)
- `@code-review-excellence`
