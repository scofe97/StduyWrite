# 09-02 §7 — 지표·추적·metadata 셋에 붙이는 데 드는 손의 크기가 다르다.
# 원문 근거: 지표 — "As part of your OnStartup calls, you must register your metrics with the
#            Prometheus libraries." / 추적 — "most plug-ins need to do exactly nothing. The
#            plugin.NextOrFailure function that most plug-ins use to call the next plug-in takes
#            care of basic integration." / metadata — "This consists of a single function,
#            Metadata" 까지만 근거로 쓴다. 이어지는 "that accepts the same parameters as ServeDNS"
#            는 원서의 오류이므로(실제 시그니처는 (ctx, request.Request)) 근거로 삼지 않는다.
#            본문 §7 의 정오 블록 참조.
# 타입 스펙: type-bar — 세 대상에 드는 구현량이 서로 다르다는 것이 비교의 본체이고, 길이로만
#           그 차이가 한눈에 잡힌다. 다만 520/240/150 이라는 비율은 원서에 없는 이 노트의
#           채점이므로, 캡션에서 그 사실을 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 540
d = D(W, H, "LEARNING COREDNS · 09-02 §7",
      "셋에 붙는 데 드는 손의 크기가 다르다",
      "원서가 셋에 대해 말한 구현량을 등급으로 옮긴 것이다. 막대 길이는 이 노트의 채점이지 "
      "원서의 수치도 측정값도 아니다.",
      "주황이 가장 손이 많이 가는 자리입니다")

BX, BW = 250, 520
BARS = [
    ("metrics", "지표 내보내기", 520, "OnStartup 에서 MustRegister · 이름·라벨 규약을 지킨다", ACC),
    ("metadata", "값 공급하기", 240, "Metadata 함수 하나 · 값이 아니라 값 함수를 넣는다", MUTED),
    ("trace", "추적 붙이기", 150, "대개 아무것도 안 한다 · NextOrFailure 가 알아서 한다", OK),
]

for i, (name, what, w, note, c) in enumerate(BARS):
    y = 140 + i * 78
    d.t(BX - 16, y + 26, name, 13, c, MONO, "end", 600)
    d.tone(BX, y, w, 40, c, 4, "20", 1.3)
    d.t(BX + 14, y + 26, what, 13, c, KR, "start", 600)
    d.t(BX, y + 60, note, 11, MUTED, KR, "start")

d.line(BX, 128, BX + BW, 128, RULE, 0.8)
d.t(BX, 120, "구현량", 11, SOFT, KR, "start")
d.t(BX + BW, 120, "많음", 11, SOFT, KR, "end")

d.box(20, 386, 840, 84, PAPER, RULE, 0.8)
d.t(36, 410, "지표에만 손이 가는 이유", 12, INK, KR, "start", 600)
d.t(36, 434, "이름과 라벨을 직접 정해야 하고, 라벨이 많거나 카디널리티가 높으면 지표 시스템을 압도할 수 있다",
     11, MUTED, KR, "start")
d.t(36, 456, "8장에서 읽는 쪽으로 본 라벨 축 이야기가 만드는 쪽에서 다시 나온다", 11, MUTED, KR, "start")

d.legend(492, [("손이 가장 많이 가는 것", ACC), ("거의 안 가는 것", OK)])
d.save("09-02.integrate-three.svg")
