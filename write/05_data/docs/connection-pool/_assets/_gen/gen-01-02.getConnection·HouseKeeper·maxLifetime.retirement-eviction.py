# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""HikariCP maxLifetime 지터 감산과 소프트 퇴출 메커니즘 도식.

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
    "HIKARICP RETIREMENT · SOFT EVICTION WORKFLOW",
    "maxLifetime 지터 감산과 유휴·활성 분기 퇴출 메커니즘",
    "생성 시점 maxLifetime 무작위 지터 감산, MaxLifetimeTask 만료 시점의 softEvictConnection 및 유휴 즉시 회수·사용 중 반납 지연 회수 흐름",
    lead="동시 대량 만료를 방지하는 무작위 분산과 활성 트랜잭션 중단 없는 소프트 퇴출 구조"
)

# ── 단계 카드 4단계 배치 ──────────────────────────────────────────────
CARD_Y = 104
CARD_H = 172
CARD_W = 196
CARD_GAP = 32
X0 = 40

STEPS = [
    {
        "num": "STEP 1",
        "title": "생성 및 지터 감산",
        "sub": "createPoolEntry",
        "items": ["maxLifetime 30분 기준", "최대 25% 지터 감산", "ThreadLocalRandom 분산"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 2",
        "title": "만료 타이머 예약",
        "sub": "MaxLifetimeTask",
        "items": ["산출된 수명(lifetime) 등록", "개별 풀 항목 독자 예약", "동시 집단 만료 억제"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 3",
        "title": "소프트 퇴출 판정",
        "sub": "softEvictConnection",
        "items": ["수명 도달 시 태스크 실행", "poolEntry.markEvicted 마킹", "사용 상태 확인 후 분기"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳
    },
    {
        "num": "STEP 4",
        "title": "대체 커넥션 보충",
        "sub": "Pool Refill",
        "items": ["addBagItem 비동기 호출", "새 물리 커넥션 생성", "설정 풀 용량 정상 유지"],
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


# ── 하단 분기 구역: 유휴 즉시 회수 vs 사용 중 지연 회수 ────────────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 880
ZONE_X = 40

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측 영역: 유휴 즉시 회수 (OK)
OK_BOX_W = 412
OK_BOX_X = ZONE_X + 16
d.tone(OK_BOX_X, ZONE_Y + 14, OK_BOX_W, 76, OK, r=6, op="12", sw=1.2)
d.t(OK_BOX_X + 20, ZONE_Y + 36, "유휴 상태 즉시 회수 (Idle 상태 선점 성공)", 13, OK, KR, "start", 600)
d.t(OK_BOX_X + 20, ZONE_Y + 56, "connectionBag.reserve() 선점 성공 시 소켓 즉시 종료", 12, INK, KR, "start")
d.t(OK_BOX_X + 20, ZONE_Y + 74, "풀에서 안전하게 분리하고 백그라운드 신규 보충 트리거", 12, MUTED, KR, "start")

# 우측 영역: 사용 중 지연 회수 (WARN)
WARN_BOX_W = 412
WARN_BOX_X = OK_BOX_X + OK_BOX_W + 24
d.tone(WARN_BOX_X, ZONE_Y + 14, WARN_BOX_W, 76, WARN, r=6, op="12", sw=1.2)
d.t(WARN_BOX_X + 20, ZONE_Y + 36, "사용 중 지연 회수 (Active 트랜잭션 진행 중)", 13, WARN, KR, "start", 600)
d.t(WARN_BOX_X + 20, ZONE_Y + 56, "선점 실패 시 표시만 남기고 사용 중 연결은 끊지 않음", 12, INK, KR, "start")
d.t(WARN_BOX_X + 20, ZONE_Y + 74, "애플리케이션이 close() 반납 호출 시 물리 커넥션 종료", 12, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("수명 분산 단계", INFO), ("소프트 퇴출 판정", ACC), ("유휴 즉시 종료", OK), ("사용 중 지연 종료", WARN)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-02.getConnection·HouseKeeper·maxLifetime.retirement-eviction.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
