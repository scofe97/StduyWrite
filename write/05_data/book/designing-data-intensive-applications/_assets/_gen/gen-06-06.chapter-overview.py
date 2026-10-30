# 06-06 개요 — 리더리스 복제의 노드 장애 대응·쿼럼 조건·동시성 판정과 6장 세 복제 방식 종합.
# 사실 출처: 06-06 서두(L21~L23), §1(L27~L37), §2(L42~L52), §3(L55~L66), §4(L70~L80)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "06-06 · CHAPTER OVERVIEW", "리더리스 복제와 6장 세 복제 방식 지도",
      "노드 장애 대응과 쿼럼 읽기·쓰기, 동시 쓰기 감지 및 6장 복제 방식 종합의 흐름을 조망한다.",
      "장애 따라잡기 · 쿼럼 중첩 · 동시성 판정 · 복제 종합")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "노드 장애와 따라잡기", "병렬 요청과 복구",
     [("failover 부재", "모든 레플리카 동등"),
      ("read repair", "읽기 시 stale 보정"),
      ("handoff · anti-entropy", "부재 중 쓰기 보존")],
     INFO),
    ("§2", "쿼럼 읽기·쓰기", "w + r > n 중첩",
     [("w+r>n 쿼럼 조건", "최신 값 보유 노드 중첩"),
      ("가용성·지연 조절", "과반수 또는 w·r 가감"),
      ("일관성 엣지 케이스", "복원·리밸런싱·LWW")],
     INFO),
    ("§3", "동시 쓰기 판정", "인과 추적과 siblings",
     [("happens-before", "인과 선행 vs 동시 판정"),
      ("버전 번호와 siblings", "이전 읽기 기준 덮어쓰기"),
      ("version vector", "레플리카별 버전 번호")],
     ACC),
    ("§4", "6장 복제 종합", "세 복제 방식 절충",
     [("단일 리더", "단일 쓰기 · 강한 일관성"),
      ("다중 리더", "멀티리전 쓰기 · 충돌 해소"),
      ("리더리스", "failover 없음 · 약한 일관성")],
     MUTED),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 1 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 1 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if any(c in top_txt for c in "=+>") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 동시성 기법", ACC), ("정상 쿼럼 충족", OK), ("엣지 케이스 주의", WARN), ("리더리스 메커니즘", INFO), ("복제 종합 비교", MUTED)])
d.save("06-06.chapter-overview.svg")
