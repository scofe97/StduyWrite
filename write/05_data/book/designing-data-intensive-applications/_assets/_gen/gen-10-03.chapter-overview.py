# 10-03 개요 — ID 생성기와 논리 시계 전체 지도
# 사실 출처: 10-03 서두(L13~L19), §1(L23~L37), §2(L39~L53), §3(L55~L69), §4(L71~L81), §5(L83~L95)
# 원서: DDIA 2nd Edition Ch. 10 "ID Generators and Logical Clocks" (p.21~32)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 280
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "10-03 · CHAPTER OVERVIEW", "ID 생성기와 논리 시계 전체 지도",
      "물리 시계의 한계에서 논리 시계와 인과 순서, 그리고 선형화 가능 ID 생성까지의 발전 흐름",
      "분산 ID 문제 · 논리 시계 3요건 · Lamport 클럭 · HLC와 벡터 클럭 · 선형화 ID")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "공통 과제: 물리 시계 오차를 넘어 분산 노드가 합의할 수 있는 인과적·선형적 순서 보장", 12, INK, KR, "middle", 600)

CW = 156
GAP = 12
X0 = 26

cards = [
    ("§1", "분산 ID 문제", "물리 시계 한계",
     [("단일 노드 병목", "전역 순서 대 확장성"),
      ("4가지 분산 방식", "샤딩·블록·UUID·시계"),
      ("인과 역전 위험", "클럭 스큐로 순서 왜곡")],
     WARN),
    ("§2", "논리 시계 개념", "인과성 추적 원리",
     [("물리 시각 배제", "이벤트 카운터 활용"),
      ("논리 시계 3요건", "컴팩트·전순서·인과성"),
      ("인과 순서 보장", "happens-before 관계")],
     INFO),
    ("§3", "Lamport 클럭", "인과적 전순서",
     [("카운터·노드ID", "동점 시 사전 순 정렬"),
      ("최댓값 기반 갱신", "max(로컬, 수신) + 1"),
      ("선형성 미보장", "동시 이벤트 구별 불가")],
     ACC),
    ("§4", "HLC · 벡터", "동시성·물리시각",
     [("하이브리드 시계", "물리 시각과 결합"),
      ("MVCC 스냅샷", "CockroachDB 적용"),
      ("벡터 클럭 O(N)", "동시 쓰기 충돌 감지")],
     OK),
    ("§5", "선형화 ID", "Timestamp Oracle",
     [("비선형화 위험", "보안 설정 우회 노출"),
      ("중앙 오라클", "TiDB Percolator 배치"),
      ("단일 노드 병목", "넘으려면 합의 (10-04)")],
     BAD),
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

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 24, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 10, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 11, SOFT, KR, "middle")
    d.line(x + 10, PY + 56, x + CW - 10, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 66

        if j == 0:
            d.tone(x + 8, iy, CW - 16, 54, card_c, 5, "14", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 11, card_c, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif is_focal and j == 1:
            d.tone(x + 8, iy, CW - 16, 54, ACC, 5, "20", 1.3)
            d.t(x + CW / 2, iy + 22, top_txt, 11, ACC, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif j == 1:
            d.box(x + 8, iy, CW - 16, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(4):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

# 범례 (5개 절 컴팩트 배치)
legend_items = [
    ("분산 ID (§1)", WARN),
    ("논리 시계 (§2)", INFO),
    ("Lamport (§3, focal)", ACC),
    ("HLC·벡터 (§4)", OK),
    ("선형화 ID (§5)", BAD),
]
d.line(12, LEG, W - 48, LEG, RULE, 0.8)
d.t(12, LEG + 22, "LEGEND", 8, SOFT, MONO, "start")
lx = 76
for lab, c in legend_items:
    d.o.append(f'<rect x="{lx}" y="{LEG + 12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(lx + 20, LEG + 22, lab, 11, MUTED, KR, "start")
    # 한글 약 11px, 영문/기호 약 7px
    w_text = sum(11 if "가" <= ch <= "힣" else 7 for ch in lab)
    lx += 26 + w_text + 14

d.save("10-03.chapter-overview.svg")
