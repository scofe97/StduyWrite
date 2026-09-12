# 타입 스펙: type-process
# 단계 여섯이 같은 자리(표 · 경로 · 결과)를 반복하므로 stage framework 다.
# 레이아웃 공식: top(i) = TOP + i*(RH+GAP), mid(i) = top(i) + RH/2
# 열 경계는 오른쪽부터 역산한다 — 결과 문구가 가장 길어 폭을 먼저 확보한다.
from dd import D, OK, BAD, WARN, INFO, MUTED, SOFT, INK, ACC, MONO, KR, PAPER2, RULE

W = 1000
TOP, RH, GAP, N = 118, 84, 8, 6
H = TOP + N * (RH + GAP) + 64
top = lambda i: TOP + i * (RH + GAP)
mid = lambda i: top(i) + RH / 2

TX = 52                        # 표 내용 시작
PX, BW, BH, STEP = 388, 58, 28, 100
NS1, BR0, NS2 = PX, PX + STEP, PX + 2 * STEP
RX = NS2 + BW + 18             # 결과 = ns2 상자 오른쪽 끝 + 여백
CX = BR0 + BW / 2              # 브리지 중심
DIE_Y = lambda yc: yc + BH / 2 + 15   # ✕ 는 상자 아래로 — 라벨과 겹치지 않게

d = D(W, H, "SECTION 5.3 LAB · FLOW TABLE STATES",
      "표를 한 줄 바꿀 때마다 패킷의 운명이 바뀝니다",
      "흐름 표의 여섯 상태와 그때 패킷이 어디서 끝나는지. 왼쪽이 표에 든 줄, 가운데가 경로, "
      "오른쪽이 결과다. 초록은 도착, 빨강은 폐기, 노랑은 세어지기는 하지만 도착하지 않는 것이다.",
      "왼쪽이 표에 든 줄, 가운데가 그때의 경로, 오른쪽이 결과입니다")

d.t(TX, 102, "흐름 표", 11, SOFT, KR, "start")
d.t(PX, 102, "경로", 11, SOFT, KR, "start")
d.t(RX, 102, "어디서 끝나나", 11, SOFT, KR, "start")

rows = [
    ("1", "priority=0 actions=NORMAL", "fail_mode 기본값이 깔아 둔 줄",
     OK,   "both",      "도착 — 옛 L2 경로에 맡깁니다"),
    ("2", "(비어 있음)", "del-flows 로 비운 뒤",
     BAD,  "die_out",   "폐기 — 올려보낼 컨트롤러가 없습니다"),
    ("3", "in_port=1 → output:2", "한 방향만 넣었을 때",
     BAD,  "die_back",  "ARP 응답이 죽어 시작조차 못 합니다"),
    ("4", "arp,in_port=2 → drop", "돌아오는 ARP 만 세어 버립니다",
     WARN, "count_die", "84 바이트가 세어짐 — 답은 왔습니다"),
    ("5", "in_port=1 → CONTROLLER", "Packet-in 으로 올려보냅니다",
     WARN, "up",        "올라가지만 답이 없어 끝납니다"),
    ("6", "tcp,tp_dst=9090 → drop", "TCP 포트로 일치를 겁니다",
     INFO, "split",     "8080 은 도착, 9090 은 침묵"),
]

for i, (num, rule, note, col, kind, result) in enumerate(rows):
    y, yc = top(i), mid(i)
    d.box(12, y, W - 24, RH, PAPER2 if i % 2 == 0 else "#0D1117", RULE, 0.9)
    d.chip(30, yc, num, col, 11)
    d.t(TX, yc - 5, rule, 11, INK, MONO, "start", 600)
    d.t(TX, yc + 14, note, 11, MUTED, KR, "start")

    for x, lab in ((NS1, "ns1"), (BR0, "br0"), (NS2, "ns2")):
        d.box(x, yc - BH / 2, BW, BH, "#0D1117", RULE, 0.9, 5)
        d.t(x + BW / 2, yc + 4, lab, 11, ACC if x == BR0 else INK, MONO, "middle", 600)

    a, b = NS1 + BW, BR0
    c, e = BR0 + BW, NS2

    if kind == "both":
        for y1, y2, m in ((a, b, 1), (c, e, 1), (e, c, -1), (b, a, -1)):
            pass
        d.arrow([(a, yc - 6), (b, yc - 6)], OK, "ok", 1.5)
        d.arrow([(c, yc - 6), (e, yc - 6)], OK, "ok", 1.5)
        d.arrow([(e, yc + 8), (c, yc + 8)], OK, "ok", 1.5)
        d.arrow([(b, yc + 8), (a, yc + 8)], OK, "ok", 1.5)
    elif kind == "die_out":
        d.arrow([(a, yc), (b, yc)], OK, "ok", 1.5)
        d.t(CX, DIE_Y(yc), "✕ 폐기", 11, BAD, KR)
    elif kind == "die_back":
        d.arrow([(a, yc - 6), (b, yc - 6)], OK, "ok", 1.5)
        d.arrow([(c, yc - 6), (e, yc - 6)], OK, "ok", 1.5)
        d.arrow([(e, yc + 8), (c, yc + 8)], BAD, "bad", 1.5)
        d.t(CX, DIE_Y(yc), "✕ 응답 폐기", 11, BAD, KR)
    elif kind == "count_die":
        d.arrow([(e, yc), (c, yc)], WARN, "warn", 1.5)
        d.chip(CX, yc - BH / 2 - 14, "n_packets=2", WARN, 9)
        d.t(CX, DIE_Y(yc), "✕ 세고 버림", 11, WARN, KR)
    elif kind == "up":
        d.arrow([(a, yc), (b, yc)], OK, "ok", 1.5)
        d.arrow([(CX, yc - BH / 2 - 2), (CX, yc - BH / 2 - 20)], WARN, "warn", 1.5)
        d.t(CX + 46, yc - BH / 2 - 12, "monitor", 9, WARN, MONO, "start")
        d.t(CX, DIE_Y(yc), "답이 없다", 11, WARN, KR)
    elif kind == "split":
        d.arrow([(a, yc - 9), (b, yc - 9)], OK, "ok", 1.5)
        d.arrow([(c, yc - 9), (e, yc - 9)], OK, "ok", 1.5)
        d.chip(CX, yc - BH / 2 - 14, "tp_dst=8080", OK, 9)
        d.arrow([(a, yc + 10), (b, yc + 10)], BAD, "bad", 1.5)
        d.chip(CX, DIE_Y(yc) - 2, "tp_dst=9090 ✕", BAD, 9)

    d.t(RX, yc + 4, result, 11, MUTED, KR, "start")

d.legend(H - 46, [("도착", OK), ("폐기", BAD), ("세어짐", WARN), ("층 교차", INFO)])
print(d.save("05-04.flow-table-states.svg"))
