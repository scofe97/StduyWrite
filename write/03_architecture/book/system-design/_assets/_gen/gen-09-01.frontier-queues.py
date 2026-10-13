# 타입 스펙: type-architecture — 프론티어 안쪽 구조. 위쪽 전면 큐(우선순위)와 아래쪽 후면 큐(예의)를 존 둘로 묶고, 후면 큐 옆에 다음 접촉 시각을 쥔 힙을 둔다.
# 사실 출처: 추출본 v2.txt 2504~2518행(라우터·매핑 표·후면 큐 b1~bn·선택기·스레드)·2523~2534행(우선순위기·전면 큐 f1~fn·편향 선택),
#   PDF 142쪽 표 매핑 en.wikipedia.org → b1 · apple.com → b2 · nike.com → bn(호스트 이름은 en.wikipedia.org 로 통일),
#   힙·"직전 소요의 10 배" 간격은 Manning·Raghavan·Schütze, Introduction to Information Retrieval §20.2.3 (https://nlp.stanford.edu/IR-book/html/htmledition/the-url-frontier-1.html),
#   200 ms × 10 = 2.0 s 는 본문의 계산 예시.
# Layout conventions: 큐 상자 폭 176·높이 68, x = 96·392·688, 존 폭 864(x=48), 세로 stride 약 240(전면 y=180, 후면 y=428). 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 880
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01 §4",
      "프론티어는 전면 큐로 순서를, 후면 큐로 예의를 정한다",
      "우선순위기가 URL 을 전면 큐에 나누고, 라우터가 호스트별 후면 큐에 담으며, 힙이 그 호스트를 다시 건드려도 되는 시각을 쥔다.",
      "전면 큐는 무엇을 먼저, 후면 큐는 언제 다시")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def node(x, y, w, h, title, sub, c, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, h, c, 6, "10", 1.1)
    d.t(x + w / 2, y + h / 2 - 2, title, 14, INK, fam(title), "middle", 600)
    d.t(x + w / 2, y + h / 2 + 18, sub, 13 if fam(sub) == KR else 12, MUTED, fam(sub))


# 입력 → 우선순위기
d.chip(184, 132, "/wiki/Kay_Hagan", MUTED, 12)
d.arrow([(248, 132), (376, 132)], MUTED, "ar", 1.4)
node(380, 104, 200, 56, "우선순위기", "갱신 빈도 · PageRank", INFO)

# 전면 큐 존
d.box(48, 184, 864, 148, PAPER2, RULE, 0.9, 8)
d.t(64, 208, "전면 · 우선순위", 13, SOFT, KR, "start", 600)
for x, t, s in ((96, "f1", "우선순위별 큐"), (392, "f2", "우선순위별 큐"), (688, "fn", "우선순위별 큐")):
    node(x, 236, 176, 68, t, s, INFO)
d.t(628, 276, "…", 16, MUTED, KR)
d.arrow([(480, 164), (480, 232)], MUTED, "ar", 1.4)
d.arrow([(480, 200), (184, 200), (184, 232)], MUTED, "ar", 1.4)
d.arrow([(480, 200), (776, 200), (776, 232)], MUTED, "ar", 1.4)

# 전면 선택기
node(380, 360, 200, 56, "전면 선택기", "높은 큐를 더 자주", INFO)
d.arrow([(480, 308), (480, 356)], MUTED, "ar", 1.4)
d.path("M 184 308 L 184 328 L 480 328", MUTED, 1.4)
d.path("M 776 308 L 776 328 L 480 328", MUTED, 1.4)

# 후면 큐 존
d.box(48, 448, 864, 256, PAPER2, RULE, 0.9, 8)
d.t(64, 472, "후면 · 예의", 13, SOFT, KR, "start", 600)
node(96, 500, 176, 56, "라우터", "호스트 → 큐", OK)
d.arrow([(480, 420), (480, 440), (184, 440), (184, 496)], MUTED, "ar", 1.4)
d.tone(560, 492, 320, 88, INFO, 6, "10", 1.1)
d.t(576, 514, "매핑 표", 13, SOFT, KR, "start", 600)
for i, (h, q) in enumerate((("en.wikipedia.org", "b1"), ("apple.com", "b2"), ("nike.com", "bn"))):
    d.t(576, 536 + i * 18, h, 12, INK, MONO, "start")
    d.t(864, 536 + i * 18, q, 12, INK, MONO, "end")
d.arrow([(276, 528), (556, 528)], MUTED, "ar", 1.4)

for x, t, s in ((96, "b1", "en.wikipedia.org"), (392, "b2", "apple.com"), (688, "bn", "nike.com")):
    node(x, 620, 176, 68, t, s, OK)
d.arrow([(184, 560), (184, 616)], MUTED, "ar", 1.4)
d.arrow([(184, 592), (480, 592), (480, 616)], MUTED, "ar", 1.4)
d.arrow([(184, 592), (776, 592), (776, 616)], MUTED, "ar", 1.4)

# 힙과 스레드
node(96, 740, 360, 64, "힙 · 다음 접촉 시각", "b1 · 200 ms × 10 = +2.0 s", OK, focal=True)
node(560, 740, 320, 64, "다운로더 스레드", "1 … N", OK)
d.arrow([(460, 772), (556, 772)], MUTED, "ar", 1.4)
d.arrow([(184, 692), (184, 720), (720, 720), (720, 736)], MUTED, "ar", 1.4)
d.path("M 480 692 L 480 720", MUTED, 1.4)
d.path("M 776 692 L 776 720 L 720 720", MUTED, 1.4)

d.legend(H - 40, [("우선순위 큐", INFO), ("호스트별 큐", OK), ("예의를 정하는 값", ACC)])
d.save("09-01.frontier-queues.svg")
