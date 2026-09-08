# 09-01 §2 — 같은 I/O 를 커널과 디스크가 각각 어디서부터 재는가.
# 타입 스펙: type-process — 시간축 위에서 구간이 반복되는 구간 지도.
#           축약: 주체(lane)가 없는 구간 지도라 §1 lanes 와 §2 공식을 쓰지 않고
#           눈금 x 를 stride 로 고정해 막대를 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 544
AXIS, BAR_Y, BAR_H, STRIDE = 132, 172, 32, 44

T = {"create": 140, "issue": 372, "done": 700}

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-01 §2",
       "커널과 디스크는 같은 I/O 를 다르게 잰다",
       "커널은 I/O 를 만든 순간부터, 디스크는 자기 큐에 들어온 순간부터 잰다. 그래서 블록 I/O 서비스 시간과 디스크 요청 시간이 같은 구간을 가리킨다.",
       "'서비스 시간' 은 OS 가 디스크를 직접 관리하던 시절의 이름입니다")

for k in T:
    d.line(T[k], AXIS + 8, T[k], BAR_Y + 4 * STRIDE + 8, RULE, 1.0, "3 6")
for k, lab in (("create", "I/O 생성 · 커널 큐"), ("issue", "디스크로 발행"), ("done", "완료 인터럽트")):
    d.t(T[k], AXIS, lab, 13, SOFT, KR, "middle")

BARS = [
    ("블록 I/O 대기", "create", "issue", "커널 큐에서 기다린 시간", None),
    ("블록 I/O 서비스", "issue", "done", "디스크에 맡긴 뒤의 시간", ACC),
    ("블록 I/O 요청", "create", "done", "커널이 보는 전체", None),
]
for i, (name, a, b, note, c) in enumerate(BARS):
    y = BAR_Y + i * STRIDE
    x1, x2 = T[a], T[b]
    if c: d.tone(x1, y, x2 - x1, BAR_H, c, 6)
    else: d.box(x1, y, x2 - x1, BAR_H, PAPER2, RULE, 1.0, 6)
    d.t(x1 - 12, y + 21, name, 13, c if c else INK, KR, "end", 600)
    d.t(x2 + 12, y + 21, note, 13, c if c else MUTED, KR, "start")

# 디스크 기준 — 같은 구간을 둘로 쪼갠다
y = BAR_Y + 3 * STRIDE + 12
d.t(T["create"] - 12, y + 21, "디스크 요청", 13, ACC, KR, "end", 600)
mid = T["issue"] + (T["done"] - T["issue"]) // 3
d.tone(T["issue"], y, mid - T["issue"], BAR_H, INFO, 6)
d.t(T["issue"] + 12, y + 21, "온디스크 큐", 13, INFO, KR, "start")
d.tone(mid, y, T["done"] - mid, BAR_H, OK, 6)
d.t(mid + 12, y + 21, "실제 처리", 13, OK, KR, "start")

YB = y + STRIDE + 20
d.t(132 - 12, YB, "온디스크 큐와 실제 처리를 더한 것이 곧 블록 I/O 서비스 시간입니다 — 같은 구간을 양쪽이 다른 이름으로 부릅니다", 13, MUTED, KR, "start")
d.t(132 - 12, YB + 24, "지금 디스크는 자체 큐를 가져, OS 가 보는 서비스 시간에 커널 큐 대기가 섞입니다", 13, MUTED, KR, "start")
d.t(132 - 12, YB + 48, "그래서 옛 iostat 의 svctm 은 부정확해져 최신판에서 빠졌습니다", 13, SOFT, KR, "start")

d.legend(YB + 72, [("커널과 디스크가 겹쳐 보는 구간", ACC), ("디스크 큐 대기", INFO), ("디스크가 실제로 처리", OK)])
d.save("09-01.io-time-terminology.svg")
