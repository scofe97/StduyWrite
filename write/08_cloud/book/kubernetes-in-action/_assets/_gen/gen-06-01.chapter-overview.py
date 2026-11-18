# 06-01 개요 — Pod status 는 주체마다 다른 시점에 채운다
# 본문: 흐름 뼈대 절의 단계 표 — "생성 → 스케줄링 → 샌드박스·init → 컨테이너 시작 → 준비 확인"
#       각 단계에서 누가 무엇을 채우는지, phase 가 언제 Pending 에서 Running 으로 바뀌는지.
# 타입 스펙: type-process.md — 주체 여럿이 순서대로 넘겨받는 처리라 위 줄은 주체, 아래 줄은
#           그 주체가 채우는 status 값이다. 같은 열은 같은 단계다. 맨 아래 막대는 phase 가
#           그 시간축 위에서 머무는 구간이라 간트 골격(구간 막대)을 빌린다.
# 연결선은 직각만 쓴다. stride 192 = 172 + 20, 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 556
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "Pod status 는 주체마다 다른 시점에 채운다",
      "API 서버가 Pod 를 받으면 phase 는 Pending 이다. 스케줄러·kubelet·probe 가 차례로 conditions 와 "
      "컨테이너 상태를 채우고, 주 컨테이너가 모두 시작되면 phase 가 Running 이 되며 Ready 는 그 뒤에 선다.",
      lead="phase 는 한 번 바뀌고, Ready 는 phase 가 Running 이 된 뒤에야 선다")

BW, GAP, X0 = 172, 20, 30
CX = [X0 + BW // 2 + i * (BW + GAP) for i in range(5)]
TOP_Y, TOP_H = 156, 68
BOT_Y, BOT_H = 260, 112
BAR_Y = 412

ddx.band(d, 104, 492, "같은 열은 같은 단계 — 위는 누가, 아래는 무엇이 채워지나")

ACTORS = [
    ("API 서버", "Pod 를 받아 저장", MUTED),
    ("스케줄러", "노드를 골라 바인딩", INFO),
    ("kubelet", "샌드박스 · init 실행", INFO),
    ("kubelet", "주 컨테이너 시작", INFO),
    ("kubelet · probe", "readiness 결과 반영", ACC),
]
VALUES = [
    ["phase: Pending"],
    ["PodScheduled: True"],
    ["PodReadyToStartContainers", "Initialized: True"],
    ["state: running", "phase: Running"],
    ["ready: true", "ContainersReady: True", "Ready: True"],
]

for i, ((name, sub, c), vals) in enumerate(zip(ACTORS, VALUES)):
    cx = CX[i]
    focal = c is ACC
    x = cx - BW // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{TOP_Y}" width="{BW}" height="{TOP_H}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, TOP_Y, BW, TOP_H, PAPER2, c, 1.1, 6)
    d.t(cx, TOP_Y + 28, ddx.fit(name, 13, BW - 16, name), 13, c if focal else INK, KR, "middle", 600)
    d.t(cx, TOP_Y + 50, ddx.fit(sub, 11, BW - 14, sub), 11, MUTED, KR)
    d.path(f"M {cx} {TOP_Y+TOP_H+6} L {cx} {BOT_Y-10}", MUTED, 1.4, m="ar")
    d.box(x, BOT_Y, BW, BOT_H, PAPER, ACC if focal else RULE, 1.4 if focal else 0.9, 6)
    for k, v in enumerate(vals):
        d.t(cx, BOT_Y + 34 + k * 28, ddx.fit(v, 10, BW - 12, v), 10, ACC if focal else INK, MONO)
    if i:
        d.path(f"M {CX[i-1]+BW//2+6} {TOP_Y+TOP_H//2} L {x-10} {TOP_Y+TOP_H//2}", MUTED, 1.5, m="ar")

# phase 구간 — 위 시간축(열) 위에 얹는다. 3열까지 Pending, 4열부터 Running.
P_END = CX[2] + BW // 2
R_START = CX[3] - BW // 2
d.o.append(f'<rect x="{X0}" y="{BAR_Y}" width="{P_END-X0}" height="32" rx="4" '
           f'fill="{INFO}22" stroke="{INFO}" stroke-width="1.0"/>')
d.t((X0 + P_END) // 2, BAR_Y + 21, "phase: Pending", 11, INFO, MONO)
d.o.append(f'<rect x="{R_START}" y="{BAR_Y}" width="{CX[4]+BW//2-R_START}" height="32" rx="4" '
           f'fill="{OK}22" stroke="{OK}" stroke-width="1.0"/>')
d.t((R_START + CX[4] + BW // 2) // 2, BAR_Y + 21, "phase: Running", 11, OK, MONO)
d.t(36, 470, "init 컨테이너가 없으면 Initialized 는 샌드박스를 만들기 전에 True 가 된다", 12, MUTED, KR, "start")
d.legend(504, [("주체", INFO), ("Pending 구간", INFO), ("Running 구간", OK), ("본문이 짚는 자리", ACC)])
d.save("06-01-chapter-overview.svg")
print("ok chapter-overview")
