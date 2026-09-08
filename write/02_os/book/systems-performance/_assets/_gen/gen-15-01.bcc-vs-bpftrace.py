# 15-01 §1 — 같은 BPF 위에 올라간 두 프론트엔드는 쓰임이 갈린다.
# 타입 스펙: type-process — 두 도구를 같은 슬롯으로 대조하는 지도.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 512
CW, CH, GAP, X0, Y = 424, 216, 32, 24, 132

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-01 §1",
       "BCC 와 bpftrace — 같은 BPF, 다른 쓰임",
       "둘 다 커널의 BPF 위에 서지만 겨냥하는 자리가 다르다. BCC 는 완성된 도구를, bpftrace 는 그 자리에서 짜는 한 줄을 준다.",
       "복잡한 도구는 BCC 로, 즉석 질문은 bpftrace 로 갑니다")

CARDS = [
    ("BCC", "완성된 도구 모음", INFO,
     ["Python 으로 프론트엔드를 짜고", "복잡한 인자·출력을 다룹니다.", "opensnoop · execsnoop 처럼", "단일 목적 도구가 수십 개입니다"],
     "남이 만든 것을 가져다 씁니다"),
    ("bpftrace", "추적의 awk", ACC,
     ["한 줄로 프로브·필터·액션을", "적어 바로 돌립니다.", "기성 도구로 답이 안 나올 때", "질문을 직접 짭니다"],
     "내가 그 자리에서 만듭니다"),
]
for i, (name, tag, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 15, c, KR, "start", 600)
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    d.line(x + 16, Y + 66, x + CW - 16, Y + 66, RULE, 0.8)
    for j, l in enumerate(body):
        d.t(x + 16, Y + 92 + j * 20, l, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "둘은 경쟁 관계가 아니라 층이 다릅니다 — bpftrace 로 답을 찾은 뒤 반복해 쓸 것을 BCC 도구로 옮기기도 합니다", 13, MUTED, KR, "start")

d.legend(YB + 24, [("즉석에서 질문을 짜는 쪽", ACC), ("완성품을 가져다 쓰는 쪽", INFO)])
d.save("15-01.bcc-vs-bpftrace.svg")
