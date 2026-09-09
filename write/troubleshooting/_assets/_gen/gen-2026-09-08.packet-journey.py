# 2026-09-08 A 문항 개념 — 패킷 하나가 커널을 지나며 네 자리를 언제 만나는가.
# 계층 그림(drop-sites)이 "어디에 있나"를 보였다면 이 그림은 "언제 지나나"를 보인다.
# 핵심은 conntrack 이 두 번 개입한다는 것 — prerouting 에서 조회하고,
# input/postrouting 끝(CONFIRM)에서 비로소 장부에 올린다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 관문 열, 각 관문에서
#           통과(오른쪽 계속)와 폐기(왼쪽 이탈)가 갈린다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 800, 700
CX, NW, NH = 250, 290, 52     # 본선 열
Y0, GAP = 116, 74
DX = 566                       # 폐기 칩 x

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 A",
      "패킷은 언제 어느 자리를 지나는가",
      "들어오는 패킷 하나가 회선에서 애플리케이션까지 가며 만나는 관문들. "
      "관문마다 상한이 있고 넘치면 오른쪽으로 조용히 빠진다. "
      "conntrack 은 두 번 개입한다 — 앞에서 조회하고, 맨 끝에서야 장부에 올린다.",
      lead="장부에 오르는 시점은 조회 시점이 아닙니다")

# (라벨, mono 부제, 폐기 라벨 or None, 색, focal)
STEPS = [
    ("NIC 링 버퍼",        "DMA · 커널이 가져감",      "링 버퍼 넘침",        INFO, False),
    ("conntrack 조회",     "prerouting · prio -200",   "테이블 꽉 참",        ACC,  True),
    ("라우팅 판정",         "내 것인가 넘길 것인가",     None,                  INFO, False),
    ("SYN 큐",             "3-way 진행 중",            "ListenDrops",         INFO, False),
    ("accept 큐",          "3-way 완료 · 앱 대기",      "ListenOverflows",     INFO, False),
    ("conntrack 확정",      "input 끝 · CONFIRM",       None,                  ACC,  True),
    ("애플리케이션",        "accept() 로 꺼내 감",       None,                  OK,   False),
]

def y(k): return Y0 + k * GAP

for k, (name, sub, drop, c, focal) in enumerate(STEPS):
    yy = y(k)
    if focal:
        d.tone(CX, yy, NW, NH, ACC, 6)
    elif k == len(STEPS) - 1:
        d.tone(CX, yy, NW, NH, OK, 6)
    else:
        d.box(CX, yy, NW, NH, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else (OK if k == len(STEPS) - 1 else INK)
    d.t(CX + 16, yy + 22, name, 13, col, KR, "start", 600)
    d.t(CX + 16, yy + 40, sub, 11, SOFT, MONO, "start")

    # 다음 관문으로
    if k < len(STEPS) - 1:
        d.arrow([(CX + NW / 2, yy + NH), (CX + NW / 2, y(k + 1) - 3)], MUTED, "ar", 1.3)

    # 폐기 분기 — 오른쪽으로 빠진다
    if drop:
        d.arrow([(CX + NW, yy + NH / 2), (DX - 4, yy + NH / 2)], BAD, "bad", 1.2, "3 3")
        d.t(DX + 6, yy + NH / 2 + 4, drop, 11, BAD, MONO, "start")

# 회선 (스택 위)
d.t(CX + NW / 2, Y0 - 18, "회선에서 도착", 12, MUTED, KR)

# conntrack 두 개입을 잇는 세로 괄호 — 조회와 확정 사이가 한 왕복
bx = CX - 34
d.path(f"M {bx+8} {y(1)+NH/2} L {bx} {y(1)+NH/2} L {bx} {y(5)+NH/2} L {bx+8} {y(5)+NH/2}", ACC, 1.1)
d.o.append(f'<text x="{bx - 12}" y="{(y(1)+y(5))/2 + NH/2}" text-anchor="middle" '
           f'font-family="{KR}" font-size="11" fill="{ACC}" '
           f'transform="rotate(-90 {bx - 12} {(y(1)+y(5))/2 + NH/2})">조회 → 등록</text>')

d.legend(H - 58, [("conntrack 이 개입하는 두 시점", ACC),
                  ("넘치면 조용히 폐기", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.packet-journey.svg"))
print("ok packet-journey")
