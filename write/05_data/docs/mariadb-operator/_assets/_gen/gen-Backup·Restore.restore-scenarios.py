# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""장애 유형별 복구 전략과 리소스 선택 경로 도식.

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
    "FAILURE RECOVERY · STRATEGY DECISION PATH",
    "장애 유형별 복구 전략과 리소스 선택 경로",
    "단일 데이터베이스 논리 실수부터 전체 클러스터 손상 및 특정 시점 롤포워드 복구 분기",
    lead="장애 영향 범위와 복구 목표 시점에 따른 선언적 복구 리소스 선택 기준"
)

# ── 3개 복구 시나리오 카드 배치 ───────────────────────────────────────
CARD_Y = 104
CARD_H = 176
CARD_W = 280
CARD_GAP = 28
X0 = 28

SCENARIOS = [
    {
        "tag": "SCENARIO 1",
        "title": "단일 데이터베이스 논리 오류",
        "sub": "테이블 또는 데이터 오작동",
        "items": [
            "적용 리소스: Restore CR",
            "동작 옵션: spec.database 단일 지정",
            "CLI 메커니즘: --one-database 복원",
            "단위: 데이터베이스 하나 (테이블 단위 없음)",
        ],
        "tone": INFO,
        "focal": False,
    },
    {
        "tag": "SCENARIO 2",
        "title": "클러스터 전면 손상 재해 복구",
        "sub": "스토리지 유실 및 신규 프로비저닝",
        "items": [
            "적용 리소스: MariaDB CR",
            "동작 옵션: spec.bootstrapFrom 선언",
            "핵심 조건: rootPassword 일치 필수",
            "영향 범위: 신규 클러스터 즉시 부트스트랩",
        ],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳
    },
    {
        "tag": "SCENARIO 3",
        "title": "바이너리 로그 시점 복구",
        "sub": "PITR (Point-In-Time-Recovery)",
        "items": [
            "기준 백업: PhysicalBackup (논리 백업 아님)",
            "적용 리소스: PointInTimeRecovery CR",
            "CLI 메커니즘: mariadb-binlog GTID 재생",
            "v26.10.2: 비동기 복제만 (Galera 미지원)",
        ],
        "tone": OK,
        "focal": False,
    },
]

for i, sc in enumerate(SCENARIOS):
    cx = X0 + i * (CARD_W + CARD_GAP)
    if sc["focal"]:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, sc["tone"], r=8, op="10", sw=1.0)

    # 상단 뱃지
    d.t(cx + CARD_W // 2, CARD_Y + 24, sc["tag"], 10, sc["tone"], MONO, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 48, sc["title"], 13, INK, KR, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 68, sc["sub"], 11, SOFT, KR, "middle")

    # 구분선
    d.line(cx + 12, CARD_Y + 80, cx + CARD_W - 12, CARD_Y + 80, RULE, 0.8)

    # 항목 목록
    for j, it in enumerate(sc["items"]):
        iy = CARD_Y + 104 + j * 20
        d.t(cx + CARD_W // 2, iy, it, 11, MUTED, KR, "middle")


# ── 하단 복구 판단 가이드 및 위험 예방 구역 ──────────────────────────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 904
ZONE_X = 28

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측 영역: 복구 시 주의점 (Root Credentials)
G1_W = 424
G1_X = ZONE_X + 16
d.tone(G1_X, ZONE_Y + 14, G1_W, 76, WARN, r=6, op="12", sw=1.2)
d.t(G1_X + 16, ZONE_Y + 36, "루트 자격 증명 일치 검증 (인증 실패 방지)", 13, WARN, KR, "start", 600)
d.t(G1_X + 16, ZONE_Y + 56, "백업 내부 비밀번호와 rootPasswordSecret 일치 필요", 12, INK, KR, "start")
d.t(G1_X + 16, ZONE_Y + 74, "불일치 시 프로브 인증 실패로 파드 재시작", 12, MUTED, KR, "start")

# 우측 영역: 부트스트랩 인식 복구 (Bootstrap Awareness)
G2_W = 424
G2_X = G1_X + G1_W + 24
d.tone(G2_X, ZONE_Y + 14, G2_W, 76, OK, r=6, op="12", sw=1.2)
d.t(G2_X + 16, ZONE_Y + 36, "부트스트랩 인식 제어 (Failover Hold)", 13, OK, KR, "start", 600)
d.t(G2_X + 16, ZONE_Y + 56, "복구 완료 전까지 Operator 가 주 노드 페일오버 전환 보류", 12, INK, KR, "start")
d.t(G2_X + 16, ZONE_Y + 74, "bootstrapFrom 이라야 적용 (단독 Restore 는 아님)", 12, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("부분 논리 복구", INFO), ("전면 부트스트랩 복구", ACC), ("시점 연속 복구", OK), ("운영 주의 검증", WARN)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "Backup·Restore.restore-scenarios.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
