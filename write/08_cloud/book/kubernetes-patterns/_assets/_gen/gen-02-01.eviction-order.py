# 02-01 축출 순서는 등급이 아니다 — kubelet 이 후보를 가르는 세 질문
# 본문: 노드 메모리가 임계에 닿으면 kubelet 은 QoS 등급이 아니라 (1) request 초과 여부
#   (2) Pod Priority (3) request 대비 초과량 순으로 축출 후보를 고른다. 예 Pod 셋의 값은 본문과 같다
#   (BestEffort request 0, Burstable request 200Mi 사용 300Mi, Guaranteed request 500Mi 사용 500Mi).
# 타입 스펙: type-flowchart — 질문마다 예·아니오 갈래가 갈리는 판정 흐름이라 마름모(질문)와
#   사각형(결과)으로 그린다. 마름모 출구는 둘뿐이다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
from ddx import fit

W, H = 1000, 548
CY = 164                         # 판정 행 중심
DW, DH = 152, 104                # 마름모
OUT_Y, OUT_H = 276, 72           # 아래 결과 상자
D_X = (208, 416, 624)            # 마름모 왼쪽 x
OW = 144

d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "축출 순서는 등급이 아니라 세 질문이 정합니다",
      "노드 메모리가 임계에 닿으면 kubelet 은 request 초과 여부, Priority, 초과량 순으로 후보를 가립니다. "
      "아래 Pod 셋은 첫 질문에서 갈리고, request 를 넘은 두 Pod 는 뒤 질문으로 이어집니다.",
      lead="QoS 등급은 이 질문들의 결과와 닮았을 뿐 kubelet 이 등급으로 순서를 정하지는 않습니다")

def diamond(x, cy, lines, c, focal=False):
    cx = x + DW // 2
    pts = f"{cx},{cy-DH//2} {x+DW},{cy} {cx},{cy+DH//2} {x},{cy}"
    if focal:
        d.o.append(f'<polygon points="{pts}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
    else:
        d.o.append(f'<polygon points="{pts}" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    for k, ln in enumerate(lines):
        lat = ln.isascii()
        d.t(cx, cy - 2 + k * 18 - (len(lines) - 1) * 9, fit(ln, 12, 80, ln), 12, c,
            MONO if lat else KR, "middle", 600)

def outbox(x, y, w, h, lines, c):
    d.box(x, y, w, h, PAPER2, c, 1.2, 6)
    for k, (ln, size, fill, wt) in enumerate(lines):
        d.t(x + w // 2, y + 24 + k * 20, fit(ln, size, w - 12, ln), size, fill,
            MONO if ln.isascii() else KR, "middle", wt)

# 시작 타원
d.o.append(f'<rect x="24" y="{CY-28}" width="136" height="56" rx="28" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(92, CY - 4, "memory.available", 11, INK, MONO, "middle", 600)
d.t(92, CY + 14, "임계 도달", 12, MUTED, KR)

# 마름모 셋
diamond(D_X[0], CY, ["usage >", "request?"], INFO, focal=True)
diamond(D_X[1], CY, ["priority", "더 낮은가?"], INFO)
diamond(D_X[2], CY, ["초과량이", "더 큰가?"], INFO)

# 시작 → Q1, 예 → 다음 질문
d.path(f"M 164 {CY} L {D_X[0]-6} {CY}", MUTED, 1.5, m="ar")
for a, b in ((0, 1), (1, 2)):
    d.path(f"M {D_X[a]+DW+4} {CY} L {D_X[b]-6} {CY}", INFO, 1.5, m="info")
    d.t((D_X[a] + DW + D_X[b]) // 2, CY - 10, "예", 12, INFO, KR, "middle", 600)

# 마지막 예 → 축출 대상
END_X = 832
d.path(f"M {D_X[2]+DW+4} {CY} L {END_X-6} {CY}", BAD, 1.5, m="bad")
d.t((D_X[2] + DW + END_X) // 2, CY - 10, "예", 12, BAD, KR, "middle", 600)
d.box(END_X, CY - 40, OW, 80, PAPER2, BAD, 1.4, 6)
d.t(END_X + OW // 2, CY - 12, "축출 대상", 14, BAD, KR, "middle", 600)
d.t(END_X + OW // 2, CY + 8, "BestEffort", 11, MUTED, MONO)
d.t(END_X + OW // 2, CY + 26, "Burstable", 11, MUTED, MONO)

# 아니오 → 아래 결과
NO = [
    ("가장 늦게",  ["Guaranteed", "500Mi = 500Mi"], OK),
    ("뒤로 밀림",  ["priority 가", "더 높음"],       MUTED),
    ("뒤로 밀림",  ["초과량이", "더 작음"],          MUTED),
]
for x, (head, sub, c) in zip(D_X, NO):
    cx = x + DW // 2
    d.path(f"M {cx} {CY+DH//2+4} L {cx} {OUT_Y-8}", c, 1.5, m="ok" if c == OK else "ar")
    d.t(cx + 12, CY + DH // 2 + 28, "아니오", 12, c if c == OK else MUTED, KR, "start", 600)
    ox = cx - OW // 2
    d.box(ox, OUT_Y, OW, OUT_H, PAPER2, c if c == OK else RULE, 1.2, 6)
    d.t(cx, OUT_Y + 24, head, 13, OK if c == OK else INK, KR, "middle", 600)
    for k, ln in enumerate(sub):
        d.t(cx, OUT_Y + 42 + k * 16, ln, 11, MUTED, MONO if ln.isascii() else KR)

# Pod 셋이 지나는 길
PY = OUT_Y + OUT_H + 52
d.t(24, PY - 14, "예 Pod 셋이 지나는 길", 12, SOFT, KR, "start", 600)
CARDS = [
    ("BestEffort", "request 0 · 사용 > 0",         "질문 1 예 → 2 → 3", BAD),
    ("Burstable",  "request 200Mi · 사용 300Mi",    "질문 1 예 → 2 → 3", BAD),
    ("Guaranteed", "request 500Mi · 사용 500Mi",    "질문 1 아니오 → 가장 늦게", OK),
]
CW, CG = 300, 24
for i, (nm, val, path, c) in enumerate(CARDS):
    x = 24 + i * (CW + CG)
    d.box(x, PY, CW, 80, PAPER2, c, 1.1, 6)
    d.t(x + 16, PY + 26, nm, 13, c, MONO, "start", 600)
    d.t(x + 16, PY + 48, val, 11, MUTED, MONO, "start")
    d.t(x + 16, PY + 68, path, 11, SOFT, KR, "start")

d.legend(PY + 104, [("첫 질문", ACC), ("판정 질문", INFO), ("축출 대상", BAD), ("가장 늦게", OK)])
d.save("02-01.eviction-order.svg")
print("ok eviction-order")
