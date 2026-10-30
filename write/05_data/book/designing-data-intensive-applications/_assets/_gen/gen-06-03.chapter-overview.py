# 06-03 개요 — 복제 지연이 깨는 세 가지 일관성 보장(read-your-writes, monotonic reads, consistent prefix reads)과 해법의 전체 지도.
# 사실 출처: 06-03 서두(L17~L21), §1(L26~L33), §2(L41~L51), §3(L56~L61), §4(L66~L72)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 276
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "06-03 · CHAPTER OVERVIEW", "복제 지연과 일관성 보장 전체 지도",
      "비동기 복제 지연으로 발생하는 세 가지 읽기 이상 현상과 각각을 방지하는 일관성 보장 체계",
      "비동기 읽기 분산 · eventual consistency · 쓰기 직후 조회 · 단조 읽기 · 인과 순서")

# 상단 배너: 공통 전제 축
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "공통 전제: 읽기 분산(read-scaling)을 위한 비동기 복제와 최종 일관성(eventual consistency)", 12, INK, KR, "middle", 600)

CW = 260
GAP = 20
X0 = 30

cards = [
    ("§2", "read-your-writes", "자기가 쓴 것은 항상 보임",
     [("이상 현상", "쓰기 직후 stale 팔로워 조회 시 유실 착각"),
      ("보장 내용", "새로고침하면 자기 갱신은 항상 보임"),
      ("구현 기법", "수정 데이터 리더 조회 · 갱신 시점 추적")],
     INFO),
    ("§3", "monotonic reads", "시간 역행 방지",
     [("이상 현상", "랙 다른 팔로워 순차 조회 시 댓글 소멸"),
      ("보장 내용", "순차 읽기에서 시간이 뒤로 가지 않음"),
      ("구현 기법", "사용자 ID 해시 기반 동일 레플리카 고정")],
     ACC),
    ("§4", "consistent prefix", "인과 순서 보존",
     [("이상 현상", "샤드별 지연 차이로 질문보다 답변 선행"),
      ("보장 내용", "쓰기가 일어난 순서 그대로 읽힘"),
      ("구현 기법", "인과 관련 쓰기를 같은 샤드에 · 인과 의존 추적")],
     OK),
]

FOCAL = 1

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 28, PY + 24, sec, card_c, 12)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 66

        if j == 0:
            d.tone(x + 10, iy, CW - 20, 54, BAD, 6, "14", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 11, BAD, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif is_focal and j == 1:
            d.tone(x + 10, iy, CW - 20, 54, ACC, 6, "20", 1.3)
            d.t(x + CW / 2, iy + 22, top_txt, 11, ACC, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif j == 1:
            d.tone(x + 10, iy, CW - 20, 54, card_c, 6, "14", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 11, card_c, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("RYW 보장 (§2)", INFO), ("단조 읽기 (§3)", ACC), ("일관된 접두사 (§4)", OK), ("읽기 이상 현상", BAD)])
d.save("06-03.chapter-overview.svg")
