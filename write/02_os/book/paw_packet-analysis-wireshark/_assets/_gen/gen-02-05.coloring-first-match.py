# 02-05 §2 — 색 규칙은 위에서부터 대조되고 먼저 걸린 규칙이 이긴다. 2번 SYN(80번 포트)은 14번 HTTP 에서 멈추고 16번 SYN(23번 포트)은 17번 SYN/FIN 까지 내려간다.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 걸리고 안 걸리는가를 규칙×프레임 격자로 본다. 축약: 스펙의 역할·컴포넌트 어휘 대신 규칙 순서×프레임 축을 쓴다(02-02 filter-direction-matrix 와 같은 선례). focal 은 2번 SYN 이 HTTP 에 걸린 셀 하나.
# 사실 출처: 노트 L124~L152 (규칙 표 L142~L150, 프레임 2·16 의 규칙 이름 L129·L134)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, COL_W, ROW_H = 408, 212, 56
COLS = [("2번", "SYN → 80번 포트"), ("16번", "SYN → 23번 포트")]
# (순서, 규칙 이름, 조건, [2번 칸, 16번 칸])  칸: no 안 걸림 · hit 걸림 · skip 대조 안 함
ROWS = [
    (1, "Bad TCP", "tcp.analysis.flags && …", ["no", "no"]),
    (6, "ARP", "arp", ["no", "no"]),
    (8, "TCP RST", "tcp.flags.reset eq 1", ["no", "no"]),
    (14, "HTTP", "http || tcp.port == 80 || http2", ["hit_acc", "no"]),
    (17, "TCP SYN/FIN", "tcp.flags & 0x02 || tcp.flags.fin == 1", ["skip", "hit_ok"]),
    (18, "TCP", "tcp", ["skip", "skip"]),
    (19, "UDP", "udp", ["skip", "skip"]),
]
X0, Y0 = 24, 128
W = X0 + LABEL_W + len(COLS) * COL_W + 24
ROW_TOP = Y0 + 40
H = ROW_TOP + len(ROWS) * ROW_H + 96

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-05 §2",
      "색 규칙이 걸리는 순서",
      "SYN 두 개가 같은 규칙 목록을 위에서부터 내려간다. 2번은 14번째 HTTP 에서 멈추고 16번만 17번째 SYN/FIN 에 닿는다.",
      "먼저 걸린 규칙 하나만 남고 아래 규칙은 대조하지 않습니다")

d.t(X0 + 8, Y0 + 4, "순서 · 규칙 · 조건", 11, SOFT, KR, "start", 600)
for j, (a, b) in enumerate(COLS):
    cx = X0 + LABEL_W + j * COL_W + (COL_W - 12) / 2
    d.t(cx, Y0 - 12, a, 12, INK, MONO, "middle", 600)
    d.t(cx, Y0 + 4, b, 11, SOFT, KR)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

for i, (order, name, cond, cells) in enumerate(ROWS):
    y = ROW_TOP + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 26, str(order), 12, SOFT, MONO, "start", 600)
    d.t(X0 + 52, y + 20, name, 13, INK, KR, "start", 600)
    d.t(X0 + 52, y + 36, cond, 11, MUTED, MONO, "start")
    for j, st in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W
        cw, ch = COL_W - 12, ROW_H - 12
        cx, cy = x + cw / 2, y + ch / 2 + 5
        if st == "hit_acc":
            d.o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(cx, cy, "걸림", 13, ACC, KR, "middle", 600)
        elif st == "hit_ok":
            d.tone(x, y, cw, ch, OK, 6)
            d.t(cx, cy, "걸림", 13, OK, KR, "middle", 600)
        elif st == "no":
            d.box(x, y, cw, ch, PAPER2, RULE, 1.0, 6)
            d.t(cx, cy, "안 걸림", 12, MUTED, KR)
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="none" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
            d.t(cx, cy, "대조 안 함", 12, SOFT, KR)

d.legend(H - 72, [("2번이 걸린 규칙", ACC), ("16번이 걸린 규칙", OK), ("안 걸림", MUTED), ("대조 안 함", SOFT)])
d.save("02-05.coloring-first-match.svg")
