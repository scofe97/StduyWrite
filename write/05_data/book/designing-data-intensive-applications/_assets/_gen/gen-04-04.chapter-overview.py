# 04-04 개요 — 보조 인덱스의 비유일 키 해소에서 출발해 인덱스에 값을 두는 세 방식과 인메모리 저장으로 이어지는 4-4 편 전체 지도.
# 사실 출처: 04-04 본문 §1(L36~L40), §2(L49~L59), §3(L66~L70)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 96
PH = 284
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-04 · CHAPTER OVERVIEW", "보조 인덱스와 인메모리 저장 전체 지도",
      "기본키 외 컬럼 검색을 위한 보조 인덱스에서 인덱스 리프의 값 저장 방식, 그리고 디스크 제약을 넘어선 인메모리 엔진으로의 확장 흐름을 조망한다.",
      "보조 인덱스 → 값 저장 방식(clustered · heap · covering) → 인메모리 엔진")

# 3개 절 컬럼 좌표
CW = 264
GAP = 16
X0 = 24

cards = [
    ("§1", "보조 인덱스", "기본키 외 컬럼 검색",
     [("1:N 비유일 키", "동일 키에 여러 행 대응"),
      ("postings list", "행 식별자 리스트 매핑"),
      ("행 ID 덧붙임", "복합키로 고유 항목 생성"),
      ("저장 엔진", "B-tree 및 로그 구조화 활용")],
     INFO),
    ("§2", "값 저장 방식", "clustered · heap · covering",
     [("clustered", "실제 행을 인덱스 안에 저장"),
      ("heap file 참조", "위치 참조 · 순서 없는 힙"),
      ("covering index", "일부 컬럼 포함 · 인덱스 응답"),
      ("갱신 트레이드오프", "제자리 덮어쓰기 · forwarding pointer")],
     ACC),
    ("§3", "인메모리 저장", "모든 데이터를 메모리에",
     [("전면 메모리 배치", "RAM 가격 하락과 소형 데이터셋"),
      ("진짜 속도 요인", "디스크 인코딩 오버헤드 제거"),
      ("내구성 확보", "append-only 로그 · 스냅샷 · 복제"),
      ("풍부한 모델", "우선순위 큐 · 집합 자료구조")],
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

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 32, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 18, PY + 26, title, 14, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 14, PY + 60, x + CW - 14, PY + 60, RULE, 0.8)

    # 내부 항목 4개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 70 + j * 50

        if is_focal and j == 0:
            d.tone(x + 12, iy, CW - 24, 44, ACC, 4, "1E", 1.2)
            d.t(x + CW / 2, iy + 19, top_txt, 12, INK, MONO if any(c in top_txt for c in "abcdefghijklmnopqrstuvwxyz") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, ACC, KR, "middle")
        elif is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 44, WARN, 4, "1A", 1.1)
            d.t(x + CW / 2, iy + 19, top_txt, 12, INK, MONO if any(c in top_txt for c in "abcdefghijklmnopqrstuvwxyz") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 44, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 19, top_txt, 12, INK, MONO if any(c in top_txt for c in "abcdefghijklmnopqrstuvwxyz") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 흐름 연결 화살표
d.arrow([(X0 + CW + 2, PY + 138), (X0 + CW + GAP - 2, PY + 138)], MUTED, "ar", 1.2)
d.arrow([(X0 + 2 * CW + GAP + 2, PY + 138), (X0 + 2 * CW + 2 * GAP - 2, PY + 138)], MUTED, "ar", 1.2)

d.legend(LEG, [("보조 인덱스", INFO), ("값 저장 구조", ACC), ("인메모리 엔진", OK), ("트레이드오프", WARN)])
d.save("04-04.chapter-overview.svg")
