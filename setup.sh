#!/bin/bash

# ==============================================================================
# 🌌 Cortex Agent Infrastructure Unified Setup (v4.0)
# ==============================================================================
# 이 스크립트는 '주입(Injection)'과 '설정(Setup)'을 단일 명령으로 통합합니다.
# 1. 실행 위치가 프로젝트 루트인 경우: 자동으로 .agents 구성을 주입합니다.
# 2. 실행 위치가 .agents 내부인 경우: 환경(venv, deps, indexing)을 구축합니다.
# 사용법: ./setup.sh
# ==============================================================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[Cortex Setup]${NC} 통합 설치 프로세스를 시작합니다..."

# 1. 위치 감지 및 모드 전환
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CWD="$(pwd)"

# 실행 위치에 따른 모드 판단
if [[ "$SCRIPT_DIR" != *".agents" ]]; then
    # [인젝션 모드] 저장소 루트에서 실행된 경우
    TARGET_PROJECT="${1:-$(pwd)}"
    echo -e "${BLUE}[Cortex Injection]${NC} 프로젝트 에이전트화를 준비합니다: ${TARGET_PROJECT}"
    
    if [ ! -d "${TARGET_PROJECT}/.agents" ]; then
        echo -e "${BLUE}[Cortex Injection]${NC} '${TARGET_PROJECT}/.agents' 생성 중..."
        mkdir -p "${TARGET_PROJECT}/.agents"
    fi
    
    echo -e "${BLUE}[Cortex Injection]${NC} 인프라 파일을 주입하는 중..."
    # 자기 자신을 포함한 모든 필요한 파일을 복사
    cp -r "$SCRIPT_DIR"/* "${TARGET_PROJECT}/.agents/"
    
    echo -e "${GREEN}[Cortex Injection]${NC} 주입 완료. 내부 설정을 계속합니다."
    cd "${TARGET_PROJECT}/.agents"
    chmod +x setup.sh
    exec ./setup.sh # 자기 자신을 다시 실행하여 설정 모드로 진입
fi

# [설정 모드] .agents 폴더 내부에서 실행된 경우
echo -e "${BLUE}[Cortex Setup]${NC} 환경 구축을 시작합니다 (CWD: $(pwd))"

# 2. Python 가상환경(venv) 생성
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[Cortex Setup]${NC} 가상환경(venv) 생성 중..."
    python3 -m venv venv
else
    echo -e "${GREEN}[Cortex Setup]${NC} 가상환경이 이미 존재합니다."
fi

# 3. 필수 의존성 패키지 설치
echo -e "${BLUE}[Cortex Setup]${NC} 필수 패키지 설치 중 (pip install)..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. 초기 인덱싱
echo -e "${BLUE}[Cortex Setup]${NC} 프로젝트 초기 인덱싱 수행 중..."
python3 scripts/cortex/indexer.py --force

# 5. 마무리 보고
echo -e "\n"
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN}✨ 에이전트 인프라 환경 구축이 완전히 완료되었습니다!${NC}"
echo -e "${GREEN}======================================================================${NC}"
echo -e "1. ${BLUE}MCP 서버 등록:${NC} 아래 경로를 MCP 클라이언트에 추가하세요."
echo -e "   - Command: $(pwd)/venv/bin/python3"
echo -e "   - Args: $(pwd)/scripts/cortex_mcp.py"
echo -e "\n"
echo -e "2. ${BLUE}부트스트랩 명령:${NC} 이제 에이전트에게 README의 프롬프트를 입력하세요."
echo -e "${GREEN}======================================================================${NC}"
