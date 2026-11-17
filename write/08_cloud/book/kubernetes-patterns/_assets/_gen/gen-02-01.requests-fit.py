# 02-01 스케줄러는 requests 합만 본다 — 같은 새 Pod 가 두 노드에서 갈리는 이유
# 본문: 스케줄러 필터는 노드 allocatable 에서 이미 놓인 Pod 들의 requests 합을 빼고 남은 자리에
#   새 Pod 의 requests 가 들어가는지 본다. limits 는 이 계산에 들어가지 않으므로 limits 합이
#   allocatable 을 넘어도 배치는 막히지 않는다. 막대 길이는 예시 값(1000Mi 노드)이다.
# 타입 스펙: type-bar — 노드마다 한 막대에 requests 를 누적해 남은 칸과 새 Pod 크기를 비교하는
#   양의 비교라 가로 누적 막대로 그린다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
from ddx import fit

W, H = 1000, 432
SCALE = 0.4                      # 1Mi = 0.4px → allocatable 1000Mi = 400px
BX = 200                         # 막대 시작 x
BAR_H, LIM_H = 40, 24
ALLOC = 1000
NEW_REQ = 200
NODE_STRIDE = 136
TOP = 108

d = D(W, H, "KUBERNETES PATTERNS · 02-01",
      "스케줄러는 requests 합만 봅니다",
      "allocatable 1000Mi 노드 두 개에 requests 가 쌓여 있고, requests 200Mi 인 새 Pod 가 들어갈 칸이 "
      "노드 A 에는 남고 노드 B 에는 모자랍니다. limits 합은 두 노드 모두 allocatable 을 넘지만 배치 판단에 쓰이지 않습니다.",
      lead="노드마다 allocatable 1000Mi · 새 Pod requests 200Mi 인 예시 값입니다")

def px(mi): return int(mi * SCALE)

NODES = [
    ("노드 A", [("web", 400, 700), ("api", 300, 500)], OK,  "Filter 통과"),
    ("노드 B", [("db", 500, 900), ("cache", 400, 600)], BAD, "Insufficient memory"),
]

for n, (name, pods, vc, verdict) in enumerate(NODES):
    y = TOP + n * NODE_STRIDE
    bar_y = y + 24
    lim_y = bar_y + BAR_H + 12
    # 왼쪽 머리
    d.t(24, bar_y + 18, name, 14, INK, KR, "start", 600)
    d.t(24, bar_y + 38, "allocatable 1000Mi", 11, MUTED, MONO, "start")
    d.t(24, lim_y + 16, f"limits 합 {sum(p[2] for p in pods)}Mi", 11, SOFT, MONO, "start")
    # allocatable 틀 — 새 Pod 가 넘치는 노드는 틀을 기존 requests 끝까지만 그린다.
    #   넘치는 새 Pod 상자가 틀과 반쯤 겹치면 겹침 센서가 error 로 잡는다.
    #   경계는 아래 "allocatable 끝" 세로선이 보인다.
    used = sum(p[1] for p in pods)
    frame_w = px(ALLOC) if NEW_REQ <= ALLOC - used else px(used)
    d.box(BX, bar_y, frame_w, BAR_H, PAPER, RULE, 1.0, 4)
    # requests 누적
    cur = 0
    for nm, rq, lm in pods:
        w = px(rq)
        d.tone(BX + px(cur), bar_y, w, BAR_H, INFO, 4, "18", 1.1)
        d.t(BX + px(cur) + w // 2, bar_y + 20, nm, 12, INFO, MONO, "middle", 600)
        d.t(BX + px(cur) + w // 2, bar_y + 34, f"{rq}Mi", 11, MUTED, MONO)
        cur += rq
    # 새 Pod — 남은 칸에 들어가는지
    free = ALLOC - cur
    fits = NEW_REQ <= free
    nc = OK if fits else BAD
    d.o.append(f'<rect x="{BX+px(cur)}" y="{bar_y}" width="{px(NEW_REQ)}" height="{BAR_H}" rx="4" '
               f'fill="{nc}22" stroke="{nc}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    d.t(BX + px(cur) + px(NEW_REQ) // 2, bar_y + 20, "새 Pod", 12, nc, KR, "middle", 600)
    d.t(BX + px(cur) + px(NEW_REQ) // 2, bar_y + 34, f"{NEW_REQ}Mi", 11, MUTED, MONO)
    # allocatable 끝 세로선
    d.line(BX + px(ALLOC), bar_y - 8, BX + px(ALLOC), bar_y + BAR_H + 4, SOFT, 1.0, "4 3")
    d.t(BX + px(ALLOC), bar_y - 14, "allocatable 끝", 11, SOFT, KR)
    # 남은 칸 표시
    RX = BX + px(ALLOC) + px(NEW_REQ) + 16
    d.t(RX, bar_y + 16, f"남은 칸 {free}Mi", 12, MUTED, KR, "start")
    d.t(RX, bar_y + 36, verdict, 12, vc, MONO if verdict.isascii() else KR, "start", 600)
    # limits 점선 행
    cur = 0
    for nm, rq, lm in pods:
        w = px(lm)
        d.o.append(f'<rect x="{BX+px(cur)}" y="{lim_y}" width="{w}" height="{LIM_H}" rx="3" '
                   f'fill="none" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="4 3"/>')
        d.t(BX + px(cur) + w // 2, lim_y + 16, f"{nm} {lm}Mi", 11, SOFT, MONO)
        cur += lm
    if cur > ALLOC:
        d.t(BX + px(cur) + 12, lim_y + 16, "배치에 안 씀", 11, MUTED, KR, "start")

d.legend(TOP + 2 * NODE_STRIDE + 8, [("requests", INFO), ("들어감", OK), ("넘침", BAD), ("limits", MUTED)])
d.save("02-01.requests-fit.svg")
print("ok requests-fit")
