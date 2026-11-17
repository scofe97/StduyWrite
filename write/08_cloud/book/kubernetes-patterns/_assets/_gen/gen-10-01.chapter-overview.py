# 10-01 장 개요 — 활성 하나가 교대되기까지 걸리는 시간이 방식마다 다르다
# 본문: 앱 밖 잠금(ReplicaSet·StatefulSet)은 노드 컨트롤러의 축출 시간(350초 (50초 + 300초))을 기다려야 하고,
#   앱 안 잠금(Lease)은 leaseDuration(15초)만 지나면 대기 Pod 가 넘겨받는다.
# 타입 스펙: type-timeline — 본문이 비교하는 것이 단계 수가 아니라 장애 뒤 교대까지의 경과 시간이다.
#   가로축을 초 단위 시간으로 두고 두 줄(앱 밖 / 앱 안)을 같은 눈금에 올려야 차이가 한눈에 보인다.
#   장애 전(기동·활성)은 시간이 의미 없어 축을 꺾어 왼쪽 구간에 단계만 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 456
T0 = 376                        # 장애 시각(t0) x
K = 1.5                         # 초당 px (t0 이후 구간)
def tx(sec): return T0 + sec * K

BASE_OUT, BASE_IN = 200, 360

d = D(W, H, "KUBERNETES PATTERNS · 10-01",
      "활성 하나가 교대되기까지",
      "두 줄 모두 장애 뒤에 활성이 하나 더 서야 끝납니다. 앱 밖 줄은 노드 컨트롤러가 Pod 를 축출할 때까지 350초 (50초 + 300초)를 기다리고, "
      "앱 안 줄은 Lease 의 leaseDurationSeconds 15초가 지나면 대기 Pod 가 잠금을 넘겨받습니다. 눈금은 t0 이후만 초 단위이고 장애 전 구간은 단계만 놓았습니다.",
      lead="같은 장애 t0 에서 교대까지: 앱 밖 350초 대 앱 안 15초")

# 줄 라벨 + 줄 바닥띠
for base, name, sub, c in ((BASE_OUT, "앱 밖 잠금", "ReplicaSet · StatefulSet", WARN),
                           (BASE_IN, "앱 안 잠금", "Lease · 대기 Pod 둘", ACC)):
    d.t(24, base - 104, name, 14, c, KR, "start", 600)
    d.t(24, base - 86, sub, 12, MUTED, KR, "start")

def axis(base):
    d.line(24, base, T0 - 28, base, SOFT, 1.2)             # 장애 전 구간
    d.line(T0 - 20, base - 8, T0 - 12, base + 8, MUTED, 1.2)  # 축 꺾임 표시
    d.line(T0 - 14, base - 8, T0 - 6, base + 8, MUTED, 1.2)
    d.line(T0 - 4, base, W - 24, base, SOFT, 1.2)          # t0 이후 구간

axis(BASE_OUT); axis(BASE_IN)

def dot(x, base, c, r=4):
    d.o.append(f'<circle cx="{x}" cy="{base}" r="{r}" fill="{c}"/>')

def label(x, base, up, title, sub, c=INK, anchor="middle", drop=28):
    """위(up=True)·아래 번갈아. 점에서 헤어라인으로 라벨까지 내린다."""
    if up:
        d.line(x, base - 6, x, base - drop + 6, RULE, 1.0)
        d.t(x, base - drop - 8, title, 13, c, KR, anchor, 600)
        if sub: d.t(x, base - drop + 8, sub, 12, MUTED, KR, anchor)
    else:
        d.line(x, base + 6, x, base + drop - 6, RULE, 1.0)
        d.t(x, base + drop + 12, title, 13, c, KR, anchor, 600)
        if sub: d.t(x, base + drop + 28, sub, 12, MUTED, KR, anchor)

# ── 앱 밖 줄 ────────────────────────────────────────────────
dot(80, BASE_OUT, MUTED);  label(80, BASE_OUT, True,  "Pod 하나 기동", None)
dot(208, BASE_OUT, MUTED); label(208, BASE_OUT, False, "그 Pod 가 활성", None)
dot(T0, BASE_OUT, BAD, 6); label(T0, BASE_OUT, True,  "t0 노드 분단", None, BAD)
x_nr = tx(50)
dot(x_nr, BASE_OUT, WARN); label(x_nr, BASE_OUT, False, "NotReady · 50초", "unreachable taint", WARN, "start")
x_ev = tx(350)
dot(x_ev, BASE_OUT, ACC, 6)
d.line(x_ev, BASE_OUT - 6, x_ev, BASE_OUT - 22, RULE, 1.0)
d.t(x_ev, BASE_OUT - 54, "350초 축출 · 새 Pod 생성", 13, ACC, KR, "end", 600)
d.t(x_ev, BASE_OUT - 36, "ReplicaSet 둘 · StatefulSet 대기", 12, MUTED, KR, "end")
# 교대까지 구간 화살표
d.path(f"M {T0+8} {BASE_OUT+68} L {x_ev-8} {BASE_OUT+68}", WARN, 1.5, m="warn")
d.t(620, BASE_OUT + 62, "taint 뒤 tolerationSeconds 300초 경과 후 축출", 12, WARN, KR, "start")

# ── 앱 안 줄 ────────────────────────────────────────────────
dot(80, BASE_IN, MUTED);  label(80, BASE_IN, True,  "Pod 셋 기동", None)
dot(196, BASE_IN, OK);    label(196, BASE_IN, True,  "pod-1 이 Lease 획득", None, OK)
dot(272, BASE_IN, OK);    label(272, BASE_IN, False, "renew 반복", None, OK)
dot(T0, BASE_IN, BAD, 6); label(T0, BASE_IN, True,  "t0 pod-1 중단", None, BAD, "end", 28)
x_h = tx(15)
dot(x_h, BASE_IN, ACC, 6)
d.line(x_h, BASE_IN + 6, x_h, BASE_IN + 22, RULE, 1.0)
d.t(x_h + 10, BASE_IN + 40, "pod-2 가 Lease 획득", 13, ACC, KR, "start", 600)
d.t(x_h + 10, BASE_IN + 58, "leaseDurationSeconds 15초 뒤", 12, MUTED, KR, "start")

# ── 눈금 ───────────────────────────────────────────────────
TICK_Y = 424
d.line(T0 - 4, TICK_Y, W - 24, TICK_Y, SOFT, 1.0)
for sec, lab in ((0, "t0"), (15, "15초"), (100, "100초"), (200, "200초"), (300, "300초"), (350, "350초")):
    x = tx(sec)
    d.line(x, TICK_Y - 4, x, TICK_Y + 4, SOFT, 1.0)
    d.t(x, TICK_Y + 18, lab, 12, SOFT if sec not in (15, 350) else ACC, KR if not lab.startswith("t0") else MONO)
d.t(24, TICK_Y + 18, "장애 전: 단계만", 12, SOFT, KR, "start")

d.save("10-01.chapter-overview.svg")
print("ok chapter-overview")
