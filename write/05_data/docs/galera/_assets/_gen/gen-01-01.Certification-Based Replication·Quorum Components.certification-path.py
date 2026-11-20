# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""Certification-Based Replication 트랜잭션 흐름 및 결정적 인증 도식.

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
    "GALERA REPLICATION · CERTIFICATION FLOW",
    "인증 기반 복제의 트랜잭션 수명주기와 결정적 검증",
    "클라이언트 트랜잭션 실행부터 쓰기 집합 브로드캐스트, 노드별 독립 인증 및 커밋·롤백 분기 흐름",
    lead="원격 잠금 없는 로컬 낙관 실행과 커밋 시점의 결정적 인증 테스트 구조"
)

# ── 단계 카드 5단계 배치 (가로 방향 프로세스) ─────────────────────────
CARD_Y = 104
CARD_H = 172
CARD_W = 160
CARD_GAP = 28
X0 = 36

STEPS = [
    {
        "num": "STEP 1",
        "title": "로컬 낙관 실행",
        "sub": "원격 락 배제",
        "items": ["SQL 문 실행", "로컬 스냅샷 읽기", "원격 잠금 없음"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 2",
        "title": "쓰기 집합 생성",
        "sub": "커밋 시점 수집",
        "items": ["COMMIT 호출", "변경 내용·기본 키 수집", "Write-Set 패키징"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 3",
        "title": "전역 브로드캐스트",
        "sub": "GComm 총 순서",
        "items": ["전체 노드 동시 전송", "전역 순번 seqno 부여", "동일 수신 순서"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 4",
        "title": "결정적 인증 검사",
        "sub": "투표 없는 독립 판정",
        "items": ["seqno 구간 대조", "기본 키 중복 검사", "노드별 자체 검증"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳!
    },
    {
        "num": "STEP 5",
        "title": "커밋 또는 롤백",
        "sub": "최종 트랜잭션 확정",
        "items": ["충돌 없음: 즉시 커밋", "충돌 감지: 강제 롤백", "Error 1213 반환"],
        "tone": OK,
        "focal": False,
    },
]

for i, st in enumerate(STEPS):
    cx = X0 + i * (CARD_W + CARD_GAP)
    # 카드 외곽
    if st["focal"]:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, st["tone"], r=8, op="10", sw=1.0)
    
    # 상단 단계 뱃지
    d.t(cx + CARD_W // 2, CARD_Y + 24, st["num"], 10, st["tone"], MONO, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 48, st["title"], 13, INK, KR, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 68, st["sub"], 11, SOFT, KR, "middle")

    # 구분선
    d.line(cx + 12, CARD_Y + 80, cx + CARD_W - 12, CARD_Y + 80, RULE, 0.8)

    # 항목 불릿
    for j, it in enumerate(st["items"]):
        iy = CARD_Y + 104 + j * 22
        d.t(cx + CARD_W // 2, iy, it, 11, MUTED, KR, "middle")

    # 단계 간 연결 화살표 (마지막 제외)
    if i < len(STEPS) - 1:
        ax1 = cx + CARD_W + 4
        ax2 = cx + CARD_W + CARD_GAP - 4
        ay = CARD_Y + CARD_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 하단 비교 및 분기 구역: 분기 상세 (커밋 성공 vs 충돌 실패) ─────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 888
ZONE_X = 36

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측 영역: 인증 성공 분기 (OK)
OK_BOX_W = 416
OK_BOX_X = ZONE_X + 16
d.tone(OK_BOX_X, ZONE_Y + 14, OK_BOX_W, 76, OK, r=6, op="12", sw=1.2)
d.t(OK_BOX_X + 20, ZONE_Y + 36, "인증 성공 경로 (동시성 충돌 없음)", 13, OK, KR, "start", 600)
d.t(OK_BOX_X + 20, ZONE_Y + 56, "모든 노드에서 쓰기 집합 적용 대기열 등록 후 커밋", 12, INK, KR, "start")
d.t(OK_BOX_X + 20, ZONE_Y + 74, "추가 네트워크 합의 라운드트립 없이 클라이언트에 성공 반환", 12, MUTED, KR, "start")

# 우측 영역: 인증 실패 분기 (BAD)
FAIL_BOX_W = 416
FAIL_BOX_X = OK_BOX_X + OK_BOX_W + 24
d.tone(FAIL_BOX_X, ZONE_Y + 14, FAIL_BOX_W, 76, BAD, r=6, op="12", sw=1.2)
d.t(FAIL_BOX_X + 20, ZONE_Y + 36, "인증 실패 경로 (동일 기본 키 충돌)", 13, BAD, KR, "start", 600)
d.t(FAIL_BOX_X + 20, ZONE_Y + 56, "늦게 인증된 쓰기 집합 즉시 폐기 및 로컬 트랜잭션 강제 롤백", 12, INK, KR, "start")
d.t(FAIL_BOX_X + 20, ZONE_Y + 74, "클라이언트에 ERROR 1213 교착 상태 예외 반환", 12, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("정상 처리 단계", INFO), ("핵심 인증 판정", ACC), ("커밋 완료", OK), ("인증 충돌 롤백", BAD)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-01.Certification-Based Replication·Quorum Components.certification-path.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
