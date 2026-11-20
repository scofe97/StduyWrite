# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""선언적 CR 과 Operator 리콘사일 제어 루프 구조 도식.

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
    "MARIADB OPERATOR · RECONCILE LOOP ARCHITECTURE",
    "선언적 CR 과 Operator 리콘사일 제어 루프",
    "CRD 선언부터 컨트롤러 감시, 복구 및 백업 작업 Pod 생성, 스토리지 연동 구조",
    lead="사용자 선언 명세와 클러스터 실제 상태를 일치시키는 리콘사일 루프 및 작업 격리 실행"
)

# ── 4개 수직 레이어 카드 배치 ──────────────────────────────────────────
LAYER_Y = 104
LAYER_H = 176
CARD_W = 202
CARD_GAP = 24
X0 = 24

LAYERS = [
    {
        "num": "LAYER 1",
        "title": "선언 계층 (API)",
        "sub": "Custom Resource",
        "items": ["Backup / Restore CR", "스토리지·주기 정의", "Secret 자격 증명 참조"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "LAYER 2",
        "title": "제어 루프 (Operator)",
        "sub": "Reconcile Controller",
        "items": ["API Server Watch 이벤트", "바라는 상태 대조 분석", "Job 생성 및 상태 갱신"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳
    },
    {
        "num": "LAYER 3",
        "title": "작업 실행 (Job)",
        "sub": "Ephemeral Runner",
        "items": ["독립 Pod 격리 실행", "mariadb-dump/backup", "메인 DB 부하 분리"],
        "tone": OK,
        "focal": False,
    },
    {
        "num": "LAYER 4",
        "title": "영속 스토리지 계층",
        "sub": "Backup Target",
        "items": ["S3 호환 오브젝트 스토리지", "영속 볼륨 (PVC)", "임시 스테이징 PVC"],
        "tone": WARN,
        "focal": False,
    },
]

for i, layer in enumerate(LAYERS):
    cx = X0 + i * (CARD_W + CARD_GAP)
    if layer["focal"]:
        d.tone(cx, LAYER_Y, CARD_W, LAYER_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, LAYER_Y, CARD_W, LAYER_H, layer["tone"], r=8, op="10", sw=1.0)

    # 상단 레이어 뱃지
    d.t(cx + CARD_W // 2, LAYER_Y + 24, layer["num"], 10, layer["tone"], MONO, "middle", 600)
    d.t(cx + CARD_W // 2, LAYER_Y + 48, layer["title"], 13, INK, KR, "middle", 600)
    d.t(cx + CARD_W // 2, LAYER_Y + 68, layer["sub"], 11, SOFT, KR, "middle")

    # 구분선
    d.line(cx + 12, LAYER_Y + 80, cx + CARD_W - 12, LAYER_Y + 80, RULE, 0.8)

    # 항목 불릿
    for j, it in enumerate(layer["items"]):
        iy = LAYER_Y + 104 + j * 22
        d.t(cx + CARD_W // 2, iy, it, 11, MUTED, KR, "middle")

    # 레이어 간 단방향 연결 화살표
    if i < len(LAYERS) - 1:
        ax1 = cx + CARD_W + 4
        ax2 = cx + CARD_W + CARD_GAP - 4
        ay = LAYER_Y + LAYER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 하단 상호작용 및 안전 격리 상세 구역 ─────────────────────────────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 912
ZONE_X = 24

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측 영역: 제어 루프의 책임 (Operator)
BOX1_W = 428
BOX1_X = ZONE_X + 16
d.tone(BOX1_X, ZONE_Y + 14, BOX1_W, 76, ACC, r=6, op="12", sw=1.2)
d.t(BOX1_X + 20, ZONE_Y + 36, "선언적 리소스 동기화와 생명주기 관리", 13, ACC, KR, "start", 600)
d.t(BOX1_X + 20, ZONE_Y + 56, "일회성 백업은 Job, 주기 백업은 CronJob 으로 리콘사일", 12, INK, KR, "start")
d.t(BOX1_X + 20, ZONE_Y + 74, "Job 결과를 status.conditions 의 Complete 조건으로 기록", 12, MUTED, KR, "start")

# 우측 영역: 작업 파드의 데이터베이스 연동 (Job Pod <-> MariaDB)
BOX2_W = 428
BOX2_X = BOX1_X + BOX1_W + 24
d.tone(BOX2_X, ZONE_Y + 14, BOX2_W, 76, OK, r=6, op="12", sw=1.2)
d.t(BOX2_X + 20, ZONE_Y + 36, "격리된 백업 실행과 데이터베이스 안정성 보호", 13, OK, KR, "start", 600)
d.t(BOX2_X + 20, ZONE_Y + 56, "DB 파드 내부 접속 대신 전용 Job Pod 로 덤프 및 복원 수행", 12, INK, KR, "start")
d.t(BOX2_X + 20, ZONE_Y + 74, "대용량 처리 시 스테이징 PVC 로 노드 로컬 디스크 고갈 방지", 12, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("선언 및 스펙", INFO), ("핵심 제어 루프", ACC), ("작업 실행자", OK), ("스토리지 백엔드", WARN)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "Backup·Restore.reconcile-loop.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
