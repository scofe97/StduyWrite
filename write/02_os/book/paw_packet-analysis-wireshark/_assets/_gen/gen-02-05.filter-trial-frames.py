# 02-05 §4 — 필터를 고쳐 가며 좁힐 때 프레임이 어떻게 빠지고 섞이는가. 최종 필터가 남기는 8프레임을 기준으로 각 시도의 맞음·섞임·빠짐을 센다.
# 타입 스펙: type-bar — 범주(필터)별 개수 비교. 가로 막대를 프레임 한 칸씩 쪼개 번호를 싣고, focal 은 8프레임만 남긴 마지막 필터.
# 사실 출처: 노트 L205~L273 (시도 출력 L214~L220·L229~L234·L243~L257·L266~L273)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

U, CW = 36, 32
BX, X0, Y0, ROW_H = 372, 24, 124, 64
TARGET = [2, 3, 4, 5, 6, 7, 16, 17]
# (필터, 설명, 맞음, 섞임, 빠짐, focal)
ROWS = [
    ("ip.src == <내 IP>", "출발지 고정", [2, 4, 5, 7, 16], [8], [3, 6, 17], False),
    ("(ip.src == …) && (ip.dst == …)", "목적지 추가", [2, 4, 5, 7, 16], [], [3, 6, 17], False),
    ("ip.addr == <서버 IP>", "필드를 ip.addr 로", TARGET, [10, 11, 12, 13, 14, 15], [], False),
    ("ip.addr == <내 IP> && ip.addr == <서버 IP>", "양쪽 주소를 ip.addr 로", TARGET, [], [], True),
]
W = 1000
H = Y0 + 20 + len(ROWS) * ROW_H + 96
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-05 §4",
      "필터 네 번과 남는 프레임",
      "목적지를 더해도 응답은 안 돌아온다. ip.addr 는 응답을 돌려주지만 다른 호스트를 섞고, 양쪽 주소를 걸어야 8프레임만 남는다.",
      "칸 하나가 프레임 하나이고 칸 안 숫자가 프레임 번호입니다")

d.t(X0 + 8, Y0 + 4, "적용한 필터", 11, SOFT, KR, "start", 600)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

def cell(x, y, n, kind):
    if kind == "ok": d.tone(x, y, CW, 32, OK, 4)
    elif kind == "warn": d.tone(x, y, CW, 32, WARN, 4)
    elif kind == "acc": d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="32" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else: d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="32" rx="4" fill="none" stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 3"/>')
    c = {"ok": OK, "warn": WARN, "acc": ACC, "bad": BAD}[kind]
    d.t(x + CW / 2, y + 21, str(n), 11, c, MONO, "middle", 600)

for i, (flt, hint, ok, extra, miss, focal) in enumerate(ROWS):
    y = Y0 + 32 + i * ROW_H
    d.t(X0 + 8, y + 16, flt, 12, INK, MONO, "start", 600)
    d.t(X0 + 8, y + 36, hint, 11, MUTED, KR, "start")
    x = BX
    for n in ok:
        cell(x, y, n, "acc" if focal else "ok"); x += U
    for n in extra:
        cell(x, y, n, "warn"); x += U
    shown = len(ok) + len(extra)
    for n in miss:
        cell(x, y, n, "bad"); x += U
    d.t(x + 12, y + 21, f"{shown}프레임", 12, ACC if focal else MUTED, KR, "start", 600 if focal else 400)

d.legend(H - 72, [("맞는 프레임", OK), ("다른 호스트가 섞임", WARN), ("빠진 프레임", BAD), ("양쪽 주소를 건 결과", ACC)])
d.save("02-05.filter-trial-frames.svg")
