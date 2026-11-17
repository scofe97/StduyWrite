# 02-01 흐름 뼈대 — 한 Pod 의 선언이 입장·배치·기동·압박·계획 다섯 단계에서 읽히는 길
# 본문: Ex 2-3(requests cpu 100m·memory 200Mi, limits memory 200Mi)과 Ex 2-4(PriorityClass
#   high-priority 1000)를 한 Pod 에 실었다고 놓고, 같은 값을 단계마다 누가 읽는지 따라간다.
# 타입 스펙: type-process — 선언 하나가 단계(가로)를 지나며 읽는 주체와 읽는 값이 바뀌는
#   형태라 단계 열 × 주체 칸으로 그린다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
from ddx import fit

# ── 좌표: 6열 stride 하나, 전부 4의 배수 ───────────────────────────────
W = 1000
X0, BW, GAP = 24, 136, 24
STRIDE = BW + GAP
TOP, BH = 104, 220
H = 432

d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "Pod 선언 한 장이 걷는 길",
      "한 Pod 의 requests, limits, priorityClassName 이 입장, 배치, 기동, 압박, 계획 여섯 단계에서 "
      "서로 다른 주체에게 읽힙니다. 선언 값은 그대로이고 읽는 주체와 결과가 바뀝니다.",
      lead="requests cpu 100m · memory 200Mi, limits memory 200Mi, priorityClassName high-priority 를 한 Pod 에 적은 경우")

# (단계, 주체, 색, [값 줄], 절)
STEPS = [
    ("1 선언", "개발자",           ACC,  ["requests", "100m · 200Mi", "limits 200Mi", "high-priority"], "1·2·3절"),
    ("2 입장", "API 서버",         INFO, ["LimitRange", "기본값 주입", "Quota 합산", "priority 1000"], "5·6절"),
    ("3 배치", "kube-scheduler",   INFO, ["requests 합 ≤", "allocatable", "PVC 바인딩", "자리 없으면 선점"], "2·3·5절"),
    ("4 기동", "kubelet",          INFO, ["ConfigMap 확인", "Secret 확인", "memory.max", "= 200Mi"], "2·3절"),
    ("5 압박", "커널 · kubelet",   BAD,  ["CPU throttle", "OOMKill", "노드 압박 축출"], "3·4절"),
    ("6 계획", "운영자",           OK,   ["프로파일 합산", "노드 크기 선택"], "7절"),
]

def is_lat(s): return all(ord(c) < 128 or c in '·≤=' for c in s)

for i, (step, actor, c, lines, sec) in enumerate(STEPS):
    x = X0 + i * STRIDE
    cx = x + BW // 2
    if c is ACC:
        d.o.append(f'<rect x="{x}" y="{TOP}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, TOP, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, TOP + 28, step, 14, c, KR, "middle", 600)
    d.t(cx, TOP + 52, fit(actor, 12, BW - 16, actor), 12, INK,
        MONO if is_lat(actor) else KR, "middle", 600)
    d.line(x + 12, TOP + 68, x + BW - 12, TOP + 68, RULE, 0.8)
    for k, ln in enumerate(lines):
        size = 11 if is_lat(ln) else 12
        d.t(cx, TOP + 96 + k * 28, fit(ln, size, BW - 16, ln), size,
            MUTED if k else INK, MONO if is_lat(ln) else KR)
    # 절 칩
    d.chip(cx, TOP + BH + 28, sec, SOFT, 11)
    # 단계 사이 화살표
    if i < len(STEPS) - 1:
        d.path(f"M {x+BW+4} {TOP+28} L {x+STRIDE-4} {TOP+28}", MUTED, 1.5, m="ar")

d.legend(TOP + BH + 64, [("선언", ACC), ("읽는 단계", INFO), ("압박", BAD), ("계획", OK)])
d.save("02-01.chapter-overview.svg")
print("ok chapter-overview")
