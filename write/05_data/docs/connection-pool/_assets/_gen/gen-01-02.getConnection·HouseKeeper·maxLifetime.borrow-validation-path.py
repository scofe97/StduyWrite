# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""HikariCP getConnection 대여 경로와 500ms 검증 생략 최적화 도식.

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
    "HIKARICP BORROW PATH · CONNECTION VALIDATION",
    "커넥션 대여 경로와 500ms 검증 생략 최적화",
    "getConnection 호출 시 ConcurrentBag 대여, 500ms 경과 여부에 따른 생략 구간, isConnectionDead 검증 및 ProxyConnection 래핑 흐름",
    lead="500ms 이내 재사용 커넥션의 검증 생략과 비정상 커넥션 즉시 폐기 및 재대여 분기"
)

# ── 단계 카드 5단계 배치 ──────────────────────────────────────────────
CARD_Y = 104
CARD_H = 172
CARD_W = 160
CARD_GAP = 28
X0 = 36

STEPS = [
    {
        "num": "STEP 1",
        "title": "대여 요청 진입",
        "sub": "ConcurrentBag.borrow",
        "items": ["getConnection 호출", "스레드 로컬 캐시 탐색", "공유 목록 CAS 선점"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 2",
        "title": "만료 여부 확인",
        "sub": "상태 플래그 검사",
        "items": ["isMarkedEvicted 확인", "퇴출 표시 항목 선별", "표시된 항목 폐기"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 3",
        "title": "생략 윈도우 판정",
        "sub": "500ms 임계치 대조",
        "items": ["경과 시간 측정 계산", "500ms 이하: 즉시 통과", "500ms 초과: 검증 진입"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳
    },
    {
        "num": "STEP 4",
        "title": "물리 생존 검증",
        "sub": "isConnectionDead",
        "items": ["JDBC4 isValid 호출", "testQuery 설정 시 실행", "validationTimeout 적용"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 5",
        "title": "프록시 래핑 반환",
        "sub": "ProxyConnection",
        "items": ["ProxyConnection 포장", "누수 감지 타이머 설정", "애플리케이션 전달"],
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


# ── 하단 비교 및 분기 구역: 검증 생략 고속 vs 검증 실패 폐기 ─────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 888
ZONE_X = 36

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측 영역: 고속 경로 (OK)
OK_BOX_W = 416
OK_BOX_X = ZONE_X + 16
d.tone(OK_BOX_X, ZONE_Y + 14, OK_BOX_W, 76, OK, r=6, op="12", sw=1.2)
d.t(OK_BOX_X + 20, ZONE_Y + 36, "검증 생략 고속 경로 (500ms 이내 재사용)", 13, OK, KR, "start", 600)
d.t(OK_BOX_X + 20, ZONE_Y + 56, "네트워크 왕복 검증 배제로 단일 호출 레이턴시 최소화", 12, INK, KR, "start")
d.t(OK_BOX_X + 20, ZONE_Y + 74, "추가 질의 없이 즉시 프록시 커넥션 생성 후 스레드 반환", 12, MUTED, KR, "start")

# 우측 영역: 검증 실패 폐기 경로 (BAD)
FAIL_BOX_W = 416
FAIL_BOX_X = OK_BOX_X + OK_BOX_W + 24
d.tone(FAIL_BOX_X, ZONE_Y + 14, FAIL_BOX_W, 76, BAD, r=6, op="12", sw=1.2)
d.t(FAIL_BOX_X + 20, ZONE_Y + 36, "검증 실패 폐기 경로 (비정상 물리 소켓 감지)", 13, BAD, KR, "start", 600)
d.t(FAIL_BOX_X + 20, ZONE_Y + 56, "검증 실패 시 closeConnection 으로 폐기", 12, INK, KR, "start")
d.t(FAIL_BOX_X + 20, ZONE_Y + 74, "풀 루프 복귀 후 다른 정상 커넥션 즉시 재대여", 12, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("일반 대여 단계", INFO), ("검증 생략 판정", ACC), ("정상 대여 완료", OK), ("검증 실패 폐기", BAD)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-02.getConnection·HouseKeeper·maxLifetime.borrow-validation-path.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
