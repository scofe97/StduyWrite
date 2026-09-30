# 00-01.chapter-overview — 코드 한 줄에서 FD 까지, 생성·접속·종료 세 단계
# 본문 요구(00-01 「학습 목표와 범위」 지도 문단): "열마다 Go 코드, 그 아래 syscall, 커널에 남는 것을
#           같은 자리에 두었고, 맨 아래 칩이 그 단계를 다루는 절" — 단계마다 같은 슬롯이 반복되는 형태다.
# 타입 스펙: type-process — lanes(코드·syscall·커널) × steps(생성·접속·종료). §2 공식의 구조
#           (label_col · step_slot · lane_h · node 는 lane 안 8px 여백)를 따르되, 스타일 계약의 한글 13px
#           하한 때문에 step_slot_w 112 → 272, node_w 100 → 256 으로 키웠다. viewBox 984 는 계약 범위 안이다.
# 사실 출처: gonet-lab main.go:51 · server.go:26·36·68 · client.go:33, 본문 §2 표.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

LABEL_W, SLOT, PAD = 140, 272, 28
W = LABEL_W + 3 * SLOT + PAD        # 984
HEAD, LANE_H = 128, 80
NODE_W, NODE_H = 256, 64
H = 492

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def cx(j):
    return LABEL_W + 8 + j * SLOT + NODE_W // 2

def top(k):
    return HEAD + k * LANE_H

d = D(W, H, "PROCESS · 00-01 OVERVIEW",
      "코드 한 줄에서 FD 까지",
      "gonet 서버의 소켓 수명을 생성·접속·종료 세 단계로 나누고, 단계마다 Go 코드와 그 아래 syscall, "
      "커널에 남는 것을 같은 자리에 둔 지도. 생성은 listener FD 하나, 접속은 연결마다 FD 하나를 남기고, "
      "종료는 두 소켓을 따로 닫는다. 맨 아래 칩은 그 단계를 다루는 절이다.",
      lead="단계마다 코드 → syscall → 커널에 남는 것 순서로 읽습니다.")

steps = ("1 생성", "2 접속", "3 종료")
lanes = ("Go 코드", "syscall", "커널에 남는 것")
cells = [
    ("net.Listen", "socket · bind · listen", "LISTEN 소켓 · FD 6"),
    ("ln.Accept", "accept4", "연결 소켓 · FD 7, 8"),
    ("conn.Close · ln.Close", "close", "두 소켓을 따로 반납"),
]
subs = [("main.go:51", "", "remote 없음"),
        ("server.go:36", "", "연결마다 하나씩"),
        ("server.go:26·68", "FD 마다 한 번씩", "conns 루프")]
tones = (INFO, OK, ACC)

for j, st in enumerate(steps):
    d.t(cx(j), 112, st, 14, ACC if j == 2 else MUTED, KR, "middle", 600)
for k, name in enumerate(lanes):
    d.line(LABEL_W, top(k), W - PAD, top(k), RULE, 0.8)
    d.t(24, top(k) + LANE_H // 2 + 5, name, 13, MUTED, KR, "start", 600)
d.line(LABEL_W, top(3), W - PAD, top(3), RULE, 0.8)
d.line(LABEL_W, HEAD, LABEL_W, top(3), RULE, 0.8)

for j in range(3):
    for k in range(3):
        x, y = cx(j) - NODE_W // 2, top(k) + 8
        main, sub = cells[j][k], subs[j][k]
        if k == 2:
            d.tone(x, y, NODE_W, NODE_H, tones[j], 6, "14" if j == 2 else "10", 1.4 if j == 2 else 1.0)
            c = tones[j]
        else:
            d.box(x, y, NODE_W, NODE_H)
            c = INK
        ty = y + (28 if sub else 38)
        d.t(cx(j), ty, main, 14, c, kr(main), "middle", 600)
        if sub:
            d.t(cx(j), y + 50, sub, 12, MUTED, kr(sub), "middle")
        if k < 2:
            d.arrow([(cx(j), y + NODE_H), (cx(j), top(k + 1) + 8)], SOFT, "soft", 1.2)
    if j < 2:
        yk = top(2) + 8 + NODE_H // 2
        d.arrow([(cx(j) + NODE_W // 2, yk), (cx(j + 1) - NODE_W // 2, yk)], SOFT, "soft", 1.2)

for j, sec in enumerate(("§2 코드와 FD", "§2 코드와 FD", "§3 수명")):
    d.chip(cx(j), 400, sec, ACC if j == 2 else MUTED, 12)

d.legend(432, [("listener 소켓", INFO), ("연결 소켓", OK), ("수명이 갈리는 곳", ACC)])
d.save("00-01.chapter-overview.svg")
print("ok chapter-overview")
