# 03-01.cgroup-namespace-primitives — 두 축 대비 (쓰는 양 / 보는 범위)
# 본문 요구: runC 가 생성 시점에 둘 다 만들고, 그 둘이 컨테이너 프로세스를 규정한다
# 타입 스펙: type-nested.md 의 커널 경계 링 + 두 갈래. 두 축이 대비되는 게 요점이라
#           나란히 같은 크기로 놓고 한 줄 요약을 서로 반대말로 맞춘다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 700
d = D(W, H, "runC · TWO KERNEL PRIMITIVES",
      "runC 가 만드는 두 커널 프리미티브 — 쓰는 양과 보는 범위",
      "cgroup 은 얼마나 쓸 수 있는가를, namespace 는 무엇을 볼 수 있는가를 정한다. 게스트 OS 는 없고 호스트 커널을 그대로 쓴다.",
      lead="cgroup 은 얼마나 쓸 수 있는가 · namespace 는 무엇을 볼 수 있는가")

RUNC = (500, 208)
RING = (100, 276, 800, 176)
CG, NS = (300, 364), (700, 364)
PROC = (500, 528)
BW, BH = 300, 88
PW, PH = 340, 88

def box(cx, cy, w, h, t, s, tag, c=None):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 16, ddx.fit(t, 14, w - 20, t), 14, c or INK,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 6, ddx.fit(s, 11, w - 18, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, cy + 28, ddx.fit(tag, 11, w - 16, tag), 11, c or SOFT, KR)

ddx.band(d, 104, 640, "게스트 OS 는 없다 — 호스트 커널의 기능 둘로 격리를 만든다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "Linux 커널 프리미티브 — 의사 파일시스템으로 노출", 11, INFO, off=16)

box(*RUNC, PW, PH, "runC", "생성 시점에 둘 다 만든다", "OCI low-level 런타임", ACC)
box(*CG, BW, BH, "cgroup", "CPU·Memory·Disk I/O·net_cls", "얼마나 쓸 수 있는가", WARN)
box(*NS, BW, BH, "namespace", "PID·Net·IPC·Mount·UTS·User", "무엇을 볼 수 있는가", INFO)
box(*PROC, PW, PH, "컨테이너 프로세스", "호스트 커널을 공유", "게스트 OS 없음")

# RUNC(330~670)·PROC(330~670) 의 x 범위가 CG(150~450)·NS(550~850) 와 겹치므로
# 꺾을 것 없이 곧은 세로 두 열이면 된다. 열은 420 / 580 — 링 라벨 마스크(~396)를
# 24px 비껴 서고, 위 구간과 아래 구간은 y 가 갈려 같은 열을 나눠 써도 겹치지 않는다.
COL = {CG[0]: 420, NS[0]: 580}
for (cx, cy) in (CG, NS):
    x = COL[cx]
    d.path(f"M {x} {RUNC[1]+PH//2+6} L {x} {cy-BH//2-8}", ACC, 1.5, m="acc")
    d.path(f"M {x} {cy+BH//2+6} L {x} {PROC[1]-PH//2-8}", MUTED, 1.5, m="ar")
# 라벨은 세로줄에서 8px 떼고, 위 두 개는 링 라벨 마스크(y 267~285) 아래로 내린다
d.t(412, 300, "만든다", 11, ACC, KR, "end")
d.t(588, 300, "만든다", 11, ACC, KR, "start")
d.t(412, 470, "제한", 11, MUTED, KR, "end")
d.t(588, 470, "가림", 11, MUTED, KR, "start")

d.t(36, 604, "두 축은 서로 다른 것을 정한다 — 쓰는 양을 줄여도 보이는 범위는 그대로이고, "
             "그 반대도 마찬가지다", 12, MUTED, KR, "start")
d.legend(656, [("만드는 쪽", ACC), ("쓰는 양", WARN), ("보는 범위", INFO)])
d.save("03-01.cgroup-namespace-primitives.svg")
print("ok cgroup-namespace-primitives")
