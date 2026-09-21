# 05-02 §1 — DNS 가 TCP 로 넘어가는 두 경우. 존 전송은 처음부터 TCP 이고, 보통 질의는 UDP 로 묻다가
# 응답이 한계를 넘으면 잘린 응답(TC=1)을 받고 TCP 로 다시 묻는다. 한계는 OPT 가 알린 크기, 없으면 512.
# 본문 요구: "TCP 는 응답 데이터 크기가 512바이트를 넘거나 존 전송 같은 작업에 쓰입니다"(원문) — 두 조건을
#            갈래로 가르고, EDNS(0) 가 바꾼 것은 첫째 갈래의 한계뿐임을 보인다.
# 근거: RFC 1035 §4.2.1 · RFC 1034 §4.3.5 · RFC 7766 §4 · RFC 6891 §6.2.3.
#       아래 두 줄의 수치는 2026-09-21 dig 9.10.6 · tshark 4.6.8 실측(TXT google.com @8.8.8.8).
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 방향이 핵심이라 주 흐름을 가로로 편다.
#           focal 은 TCP 로 다시 묻는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 960, 608
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §1",
      "DNS 가 TCP 로 넘어가는 두 경우",
      "존 전송은 처음부터 TCP 로 간다. 보통 질의는 UDP 로 묻고, 응답이 한계를 넘으면 서버가 잘라서 TC 비트를 세우고 클라이언트가 같은 질의를 TCP 로 다시 묻는다. 한계는 질의의 OPT 가 알린 크기이고, OPT 가 없으면 512바이트다.",
      "EDNS(0) 가 바꾸는 것은 한계 하나입니다 — 존 전송 갈래는 그대로입니다")

CY = 184                       # 주 흐름 중심
RH = 52                        # 사각 칸 높이

def oval(x, w, cy, txt, c=INK):
    d.o.append(f'<rect x="{x}" y="{cy - 20}" width="{w}" height="40" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(x + w / 2, cy + 5, txt, 13, c, kr(txt), "middle", 600)

def diamond(cx, cy, hw, hh, txt):
    d.o.append(f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 13, INK, kr(txt), "middle", 600)

def step(x, y, w, title, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    elif c:
        d.tone(x, y, w, RH, c, 6)
    else:
        d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    col = c if c else INK
    d.t(x + w / 2, y + 22, title, 13, col, kr(title), "middle", 600)
    d.t(x + w / 2, y + 40, sub, 12, MUTED, kr(sub))

# 주 흐름 — 왼쪽에서 오른쪽
D1X, D1HW, DHH = 232, 72, 32
D2X, D2HW = 656, 100
UX, UW = 368, 152              # UDP 질의 칸
EX, EW = 824, 112              # 끝 타원
oval(24, 96, CY, "DNS 질의")
d.arrow([(124, CY), (D1X - D1HW - 4, CY)], MUTED, "ar", 1.4)
diamond(D1X, CY, D1HW, DHH, "존 전송인가?")
d.arrow([(D1X + D1HW + 4, CY), (UX - 4, CY)], MUTED, "ar", 1.4)
d.t(D1X + D1HW + 12, CY - 10, "아니오", 12, MUTED, KR, "start", 600)
step(UX, CY - RH / 2, UW, "UDP 53 질의", "OPT 로 받을 크기 알림")
d.arrow([(UX + UW + 4, CY), (D2X - D2HW - 4, CY)], MUTED, "ar", 1.4)
diamond(D2X, CY, D2HW, DHH, "응답이 한계를 넘나?")
d.t(D2X, CY - DHH - 16, "한계 = OPT 크기 · 없으면 512", 12, MUTED, KR)
d.arrow([(D2X + D2HW + 4, CY), (EX - 4, CY)], OK, "ok", 1.4)
d.t(D2X + D2HW + 12, CY - 10, "아니오", 12, OK, KR, "start", 600)
oval(EX, EW, CY, "UDP 로 끝", OK)

# 아래 갈래 — 존 전송
Y_DOWN = 272
d.arrow([(D1X, CY + DHH + 4), (D1X, Y_DOWN - 4)], INFO, "info", 1.4)
d.t(D1X + 12, CY + DHH + 28, "예", 12, INFO, KR, "start", 600)
step(D1X - 100, Y_DOWN, 200, "처음부터 TCP 53", "AXFR · 존 전송", INFO)

# 아래 갈래 — 잘린 응답 뒤 TCP 로 다시
d.arrow([(D2X, CY + DHH + 4), (D2X, Y_DOWN - 4)], WARN, "warn", 1.4)
d.t(D2X + 12, CY + DHH + 28, "예", 12, WARN, KR, "start", 600)
step(D2X - 100, Y_DOWN, 200, "TC=1 잘린 응답", "답 0개 · 헤더와 질문만", WARN)
Y_TCP = Y_DOWN + RH + 36
d.arrow([(D2X, Y_DOWN + RH + 4), (D2X, Y_TCP - 4)], ACC, "acc", 1.4)
step(D2X - 100, Y_TCP, 200, "TCP 53 으로 다시 묻기", "같은 질의 · 전체 응답", focal=True)

# 실측 두 줄 — 같은 질의가 OPT 유무로 갈린다
Y_T = Y_TCP + RH + 60
COLS = [48, 232, 432, 600]
d.line(24, Y_T - 24, W - 24, Y_T - 24, RULE, 0.8)
d.t(24, Y_T - 32, "TXT google.com @8.8.8.8 · 2026-09-21 dig 실측", 12, SOFT, KR, "start", 600)
ROWS = [
    ("dig +noedns", "OPT 없음 · 한계 512", "응답 1,176B", "TC=1 → TCP 53 · 답 17개", WARN),
    ("dig (기본)",  "OPT 4096",          "응답 1,187B", "UDP 한 번 · 답 17개",      OK),
]
for i, (cmd, opt, size, res, c) in enumerate(ROWS):
    y = Y_T + i * 32
    d.t(COLS[0], y, cmd, 12, INK, kr(cmd), "start", 600)
    d.t(COLS[1], y, opt, 12, MUTED, kr(opt), "start")
    d.t(COLS[2], y, size, 12, MUTED, kr(size), "start")
    d.t(COLS[3], y, res, 12, c, kr(res), "start", 600)

d.legend(H - 56, [("TCP 로 다시 묻는 자리", ACC), ("잘린 응답", WARN), ("처음부터 TCP", INFO), ("UDP 로 끝", OK)])
d.save("05-02.dns-tcp-fallback.svg")
