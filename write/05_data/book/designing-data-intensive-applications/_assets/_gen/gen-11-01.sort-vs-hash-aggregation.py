# 11-01 §4 — 인메모리 해시 집계와 외장 정렬 기반 집계의 선택 기준, 동작 메커니즘, 디스크 스필 대조.
# 사실 출처: 11-01 본문 §3(L78~L81), §4(L86~L95), DDIA 2판 Ch 11 p.6~7 ("Sorting Versus In-Memory Aggregation"). 칸 라벨은 본문 및 원서 대목.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 260
BOT_Y = PY + PH + 16
BOT_H = 40
LEG = BOT_Y + BOT_H + 20
H = LEG + 52

d = D(W, H, "11-01 · §4 AGGREGATION COMPARISON", "정렬 vs 인메모리 집계 선택 기준과 메커니즘",
      "워킹셋 크기와 메모리 용량에 따른 두 집계 방식을 비교한다. 워킹셋이 메모리를 넘을 때 외장 정렬과 디스크 스필이 안정성을 보장하며, 병목은 디스크 순차 읽기다.",
      "워킹셋 크기 기준 선택 · 인메모리 O(1) vs 디스크 스필 병합 정렬 · 순차 I/O 읽기 병목")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "워킹셋 정의: 로그 파일의 총 행 수가 아니라 고유 키(URL) 수 × 카운터 크기", 12, INK, KR, "middle", 600)

PW = 404
GAP = 16
X0 = 28

panels = [
    ("인메모리 해시 집계", "Python defaultdict 방식", INFO, False, [
        ("적용 전제", "워킹셋 ≤ 가용 메모리", "고유 키 수가 적은 트래픽 분포에 적합"),
        ("동작 방식", "O(1) 임의 접근 카운터 갱신", "정렬 오버헤드 없음 · 메모리 내 연산"),
        ("한계·위험", "메모리 초과 시 디스크 스왑", "워킹셋 초과 시 OOM 또는 급격한 성능 저하"),
    ]),
    ("정렬 기반 집계", "Unix sort | uniq 방식", ACC, True, [
        ("적용 전제", "워킹셋 > 가용 메모리", "고유 키가 균일하게 분산된 대용량 처리에 적합"),
        ("동작 방식", "외장 병합 정렬 · 디스크 스필", "메모리 임계 초과 시 자동 세그먼트 분할"),
        ("핵심 장점", "순차 I/O 활용 · 대규모 처리", "메모리 용량을 초과하는 대규모 로그 안정 처리"),
    ]),
]

for i, (title, sub, c, is_focal, items) in enumerate(panels):
    x = X0 + i * (PW + GAP)

    # 외곽 상자
    if is_focal:
        d.box(x, PY, PW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, PW, PH, PAPER2, RULE, 0.9)

    # 헤더
    d.t(x + 20, PY + 26, title, 14, c if is_focal else INK, KR, "start", 600)
    d.t(x + PW - 20, PY + 26, sub, 11, MUTED, KR, "end")
    d.line(x + 10, PY + 42, x + PW - 10, PY + 42, RULE, 0.8)

    # 3개 항목
    for j, (tag, h_txt, d_txt) in enumerate(items):
        iy = PY + 52 + j * 64
        if is_focal:
            d.tone(x + 12, iy, PW - 24, 54, ACC, 4, "10", 0.9)
        else:
            d.box(x + 12, iy, PW - 24, 54, PAPER, RULE, 0.8)

        d.chip(x + 50, iy + 27, tag, c, 11, 4)
        d.t(x + 98, iy + 21, h_txt, 12, INK if is_focal else MUTED, KR, "start", 600 if is_focal else 400)
        d.t(x + 98, iy + 41, d_txt, 11, MUTED, KR, "start")

# 하단 공통 병목 배너
d.tone(28, BOT_Y, W - 56, BOT_H, WARN, 4, "14", 1.0)
d.t(W / 2, BOT_Y + 24, "실제 성능 병목: 대부분 정렬 연산 자체가 아니라 입력 파일의 순차 디스크 읽기 속도(I/O 대역폭)", 11.5, INK, KR, "middle", 600)

d.legend(LEG, [
    ("인메모리 해시 집계", INFO),
    ("정렬 기반 집계 (focal)", ACC),
    ("공통 성능 병목", WARN),
])

d.save("11-01.sort-vs-hash-aggregation.svg")
