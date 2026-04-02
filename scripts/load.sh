#!/bin/bash

# 프로젝트 정보 설정
PROJECT_ROOT="$(pwd)"
PROJECT_NAME=$(basename "$PROJECT_ROOT")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 백업 및 로드 경로 설정
AGENT_DIR=".agents"
SKILLS_DIR="skills"
GDRIVE_LATEST="gdrive:AgentBackups/${PROJECT_NAME}/latest/${PROJECT_NAME}_backup_latest.tar.gz"
LATEST_BACKUP_FILE="${PROJECT_NAME}_backup_latest.tar.gz"

echo "=========================================="
echo "[INFO] 고속 단일 압축 복구(Load)를 시작합니다."
echo "[INFO] 프로젝트: ${PROJECT_NAME}"
echo "[INFO] 파일: ${GDRIVE_LATEST}"
echo "=========================================="

# 1. 기존 데이터 백업 (안전을 위해 아카이브 생성)
BACKUP_DIR=".agents_archive/backup_${TIMESTAMP}"
mkdir -p ".agents_archive"
if [ -d "${AGENT_DIR}" ] || [ -d "${SKILLS_DIR}" ]; then
    echo "[PROGRESS] 기존 데이터 백업 중: ${BACKUP_DIR}"
    mkdir -p "${BACKUP_DIR}"
    [ -d "${AGENT_DIR}" ] && mv "${AGENT_DIR}" "${BACKUP_DIR}/"
    [ -d "${SKILLS_DIR}" ] && mv "${SKILLS_DIR}" "${BACKUP_DIR}/"
fi

# 2. 최신 압축 파일 다운로드 (단일 전송)
echo "[PROGRESS] Google Drive에서 최신 백업 다운로드 중..."
rclone copy "${GDRIVE_LATEST}" "." --progress

if [ ! -f "${LATEST_BACKUP_FILE}" ]; then
    echo "[ERROR] 백업 파일을 불러오지 못했습니다!"
    # 원복 시도
    [ -d "${BACKUP_DIR}/${AGENT_DIR}" ] && mv "${BACKUP_DIR}/${AGENT_DIR}" "."
    [ -d "${BACKUP_DIR}/${SKILLS_DIR}" ] && mv "${BACKUP_DIR}/${SKILLS_DIR}" "."
    exit 1
fi

# 3. 압축 해제 및 복구 (venv 제외 상태로 복구됨)
echo "[PROGRESS] 지식 인프라 정착 중..."
tar -xzf "${LATEST_BACKUP_FILE}" -C "." 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[SUCCESS] 복구가 완료되었습니다."
else
    echo "[ERROR] 압축 해제 실패!"
    exit 1
fi

# 4. 임시 압축 파일 삭제
rm "${LATEST_BACKUP_FILE}"

echo "------------------------------------------"
echo "[DONE] 최종 로드 완료 (백업: ${BACKUP_DIR})"
echo "------------------------------------------"

# read -p 제거됨 (백그라운드 실행 안정화)
