# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""IST 와 SST 상태 전송 메커니즘 및 Donor 노드 부하 비교 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
좌표와 간격은 모두 4의 배수로 산출한다.
다크 스킨 토큰과 1곳의 focal 포인트를 적용한다.
"""
import pathlib
import sys

# 상위 폴더의 dd.py 임포트
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 480

d = D(
    W,
    H,
    "GALERA REPLICATION · STATE TRANSFERS",
    "IST 와 SST 의 상태 전송 경로와 Donor 영향",
    "빠진 트랜잭션만 전달하는 증분 전송과 전체 스냅샷 복사 방식의 데이터 흐름 및 잠금 차이",
    lead="GCache 기반 비차단 증분 전송(IST)과 스냅샷 백업 전송(SST)의 분기 구조"
)

# ── 상단 구역: IST 경로 (증분 상태 전송) ─────────────────────────────
TOP_Y = 104
TOP_H = 144
TOP_W = 888
X0 = 36

d.box(X0, TOP_Y, TOP_W, TOP_H, PAPER2, RULE, 0.8, r=8)

# 상단 좌측 라벨
d.tone(X0 + 16, TOP_Y + 16, 120, 28, OK, r=4, op="18", sw=1.2)
d.t(X0 + 76, TOP_Y + 34, "IST (증분 전송)", 12, OK, KR, "middle", 600)

# IST 단계 3카드 배치
IST_CARD_Y = TOP_Y + 52
IST_CARD_H = 76
IST_CARD_W = 216
IST_GAP = 28
IST_X0 = X0 + 16

IST_STEPS = [
    {
        "title": "Joiner 재연결",
        "sub": "마지막 seqno 전달",
        "desc": "클러스터 UUID 대조",
        "focal": False,
        "tone": INFO
    },
    {
        "title": "Donor GCache 조회",
        "sub": "누락 write-set 추출",
        "desc": "캐시 링 버퍼 범위 확인",
        "focal": True,  # FOCAL 1곳: GCache 조회 및 증분 추출
        "tone": ACC
    },
    {
        "title": "증분 스트리밍 적용",
        "sub": "Joiner 동기화 완료",
        "desc": "Donor 정상 쿼리 수용",
        "focal": False,
        "tone": OK
    }
]

for i, st in enumerate(IST_STEPS):
    cx = IST_X0 + i * (IST_CARD_W + IST_GAP)
    if st["focal"]:
        d.tone(cx, IST_CARD_Y, IST_CARD_W, IST_CARD_H, ACC, r=6, op="18", sw=1.6)
    else:
        d.tone(cx, IST_CARD_Y, IST_CARD_W, IST_CARD_H, st["tone"], r=6, op="10", sw=1.0)
    
    d.t(cx + IST_CARD_W // 2, IST_CARD_Y + 22, st["title"], 13, INK, KR, "middle", 600)
    d.t(cx + IST_CARD_W // 2, IST_CARD_Y + 42, st["sub"], 11, SOFT, KR, "middle")
    d.t(cx + IST_CARD_W // 2, IST_CARD_Y + 60, st["desc"], 11, MUTED, KR, "middle")

    if i < len(IST_STEPS) - 1:
        ax1 = cx + IST_CARD_W + 4
        ax2 = cx + IST_CARD_W + IST_GAP - 4
        ay = IST_CARD_Y + IST_CARD_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)

# 우측 특징 요약 카드
SUMMARY_X = IST_X0 + 3 * (IST_CARD_W + IST_GAP) - 8
SUMMARY_W = X0 + TOP_W - 16 - SUMMARY_X  # 바깥 틀 안쪽 16px 에서 끝낸다 (=132)
d.tone(SUMMARY_X, IST_CARD_Y, SUMMARY_W, IST_CARD_H, OK, r=6, op="08", sw=1.0)
d.t(SUMMARY_X + SUMMARY_W // 2, IST_CARD_Y + 24, "Donor 상태 영향", 12, OK, KR, "middle", 600)
d.t(SUMMARY_X + SUMMARY_W // 2, IST_CARD_Y + 44, "읽기·쓰기 차단 없음", 11, INK, KR, "middle")
d.t(SUMMARY_X + SUMMARY_W // 2, IST_CARD_Y + 62, "고속 상태 동기화", 11, MUTED, KR, "middle")


# ── 하단 구역: SST 경로 (스냅샷 상태 전송) ───────────────────────────
BOT_Y = 264
BOT_H = 144
BOT_W = 888

d.box(X0, BOT_Y, BOT_W, BOT_H, PAPER2, RULE, 0.8, r=8)

# 하단 좌측 라벨
d.tone(X0 + 16, BOT_Y + 16, 120, 28, WARN, r=4, op="18", sw=1.2)
d.t(X0 + 76, BOT_Y + 34, "SST (스냅샷 전송)", 12, WARN, KR, "middle", 600)

# SST 비교 카드 둘: rsync vs mariadb-backup
METHOD_CARD_Y = BOT_Y + 52
METHOD_CARD_H = 76
METHOD_CARD_W = 340
METHOD_GAP = 28

# 카드 1: rsync 방식
RSYNC_X = X0 + 16
d.tone(RSYNC_X, METHOD_CARD_Y, METHOD_CARD_W, METHOD_CARD_H, BAD, r=6, op="10", sw=1.0)
d.t(RSYNC_X + 20, METHOD_CARD_Y + 22, "rsync 방식 (기본값, 차단형 전송)", 13, BAD, KR, "start", 600)
d.t(RSYNC_X + 20, METHOD_CARD_Y + 42, "Donor 에 읽기 잠금", 11, INK, KR, "start")
d.t(RSYNC_X + 20, METHOD_CARD_Y + 60, "전송 내내 Donor 쓰기 차단", 11, MUTED, KR, "start")

# 카드 2: mariadb-backup 방식
BACKUP_X = RSYNC_X + METHOD_CARD_W + METHOD_GAP
d.tone(BACKUP_X, METHOD_CARD_Y, METHOD_CARD_W, METHOD_CARD_H, OK, r=6, op="10", sw=1.0)
d.t(BACKUP_X + 20, METHOD_CARD_Y + 22, "mariadb-backup 방식 (비차단형 물리 백업)", 13, OK, KR, "start", 600)
d.t(BACKUP_X + 20, METHOD_CARD_Y + 42, "복사 중에도 쿼리 수용", 11, INK, KR, "start")
d.t(BACKUP_X + 20, METHOD_CARD_Y + 60, "백업 끝에만 잠깐 전역 잠금", 11, MUTED, KR, "start")

# 우측 특징 요약 카드
SST_SUM_X = BACKUP_X + METHOD_CARD_W + 20
SST_SUM_W = X0 + BOT_W - 16 - SST_SUM_X  # 바깥 틀 안쪽 16px 에서 끝낸다 (=128)
d.tone(SST_SUM_X, METHOD_CARD_Y, SST_SUM_W, METHOD_CARD_H, WARN, r=6, op="08", sw=1.0)
d.t(SST_SUM_X + SST_SUM_W // 2, METHOD_CARD_Y + 24, "전환 발생 조건", 12, WARN, KR, "middle", 600)
d.t(SST_SUM_X + SST_SUM_W // 2, METHOD_CARD_Y + 44, "GCache 이력 누락 시", 11, INK, KR, "middle")
d.t(SST_SUM_X + SST_SUM_W // 2, METHOD_CARD_Y + 62, "신규 노드 최초 합류", 11, MUTED, KR, "middle")


# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 428
d.legend(LEGEND_Y, [("정상 수용 및 비차단", OK), ("핵심 캐시 추출", ACC), ("식별자 및 순번 대조", INFO), ("조건부 전송", WARN), ("잠금 및 쿼리 차단", BAD)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-02.State Transfers·Restarting the Cluster.state-transfers.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
