# 13-04 §1 — 대기 소켓 하나와 4-tuple 로 갈라지는 연결별 소켓, 그리고 로컬 주소를 묶은 대기 소켓의 대비.
# 사실 출처: 원서 §13.7.1–13.7.2 의 netstat -a -n -t 출력과 Listing 13-9.
#   위: :::22 LISTEN(원격 :::*), ESTABLISHED ::ffff:10.0.0.1:22 ↔ ::ffff:10.0.0.3:16137 · 16140,
#       PPPoE 쪽 ::ffff:67.125.227.195:22 ↔ ::ffff:169.229.62.97:1473. LISTEN 만 SYN 을, ESTABLISHED 만 데이터를 받는다.
#   아래: sock -s 10.0.0.1 8888 → 10.0.0.1:8888 LISTEN(원격 0.0.0.0:*), 10.0.0.3:16153 에서 온 연결은 ESTABLISHED.
#       127.0.0.1:8888 로 온 SYN 591843787 에는 TCP 모듈이 R 0:0(0) ack 591843788 로 답하고 애플리케이션은 요청을 보지 못한다.
#   netstat 출력은 원서에서 번호 없는 본문 예시이고, 번호가 붙은 것은 RST 를 보인 Listing 13-9 하나다.
# 타입 스펙: type-architecture — 들어오는 세그먼트(왼쪽)가 4-tuple 대조로 소켓(오른쪽)에 갈라지는 구성. 두 존이 bind 방식.
#           축약: 존 안의 소켓을 행으로 쌓아 상태 · 로컬 끝점 · 원격 끝점 세 칸을 같은 x 에 맞춘다(표처럼 읽히게).
#           focal 은 와일드카드 LISTEN 소켓 하나 — 같은 포트 22 를 지키며 새 SYN 만 받는 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 608
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-04 §1",
      "포트 하나, 소켓 여럿 — 4-tuple 로 갈라진다",
      "위는 와일드카드 주소로 22번 포트에 바인딩한 sshd 다. LISTEN 소켓 하나가 새 SYN 을 받고, 성립한 연결마다 같은 포트 22 를 쓰는 ESTABLISHED 소켓이 따로 생긴다. "
      "들어온 세그먼트는 목적지·출발지의 IP 주소와 포트 네 값으로 어느 소켓에 갈지 정해진다. 아래는 10.0.0.1:8888 에만 바인딩한 서버로, "
      "같은 호스트의 127.0.0.1:8888 로 온 SYN 은 맞는 대기 소켓이 없어 운영체제 TCP 가 RST 로 거절한다.",
      "서버 포트는 그대로이고 원격 끝점이 연결을 가릅니다")

CX, CW, CH, STRIDE = 248, 648, 36, 48
COL_STATE, COL_LOCAL, COL_FOREIGN = CX + 16, CX + 132, CX + 392
IN_X, AR0, AR1 = 24, 188, CX - 4

def zone(y, h, label):
    d.o.append(f'<rect x="16" y="{y}" width="{W - 32}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    d.t(32, y + 20, label, 12, SOFT, _kr(label), "start", 600)
    for x, lab in ((COL_STATE, "상태"), (COL_LOCAL, "로컬 끝점"), (COL_FOREIGN, "원격 끝점")):
        d.t(x, y + 20, lab, 11, SOFT, KR, "start")

def row(y, incoming, in_c, state, local, foreign, kind="box"):
    cy = y + CH / 2
    d.arrow([(AR0, cy), (AR1, cy)], in_c, {INFO: "info", MUTED: "ar"}[in_c], 1.4)
    d.t(IN_X, cy + 4, incoming, 12, in_c, _kr(incoming), "start", 600)
    if kind == "focal":
        d.o.append(f'<rect x="{CX}" y="{y}" width="{CW}" height="{CH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        sc = ACC
    elif kind == "bad":
        d.tone(CX, y, CW, CH, BAD, 6, "14", 1.2); sc = BAD
    else:
        d.box(CX, y, CW, CH, PAPER2, RULE, 0.9, 6); sc = OK
    d.t(COL_STATE, cy + 4, state, 12, sc, _kr(state), "start", 600)
    d.t(COL_LOCAL, cy + 4, local, 12, INK, _kr(local), "start")
    d.t(COL_FOREIGN, cy + 4, foreign, 12, MUTED if kind == "bad" else INK, _kr(foreign), "start")

# 위 — 와일드카드 bind
ZA = 96
zone(ZA, 4 * STRIDE + 28, "와일드카드 bind · sshd :::22")
y0 = ZA + 32
row(y0 + 0 * STRIDE, "SYN · :22", INFO, "LISTEN", ":::22", ":::*", "focal")
row(y0 + 1 * STRIDE, "데이터 · :16137", MUTED, "ESTABLISHED", "::ffff:10.0.0.1:22", "::ffff:10.0.0.3:16137")
row(y0 + 2 * STRIDE, "데이터 · :16140", MUTED, "ESTABLISHED", "::ffff:10.0.0.1:22", "::ffff:10.0.0.3:16140")
row(y0 + 3 * STRIDE, "데이터 · :1473", MUTED, "ESTABLISHED", "::ffff:67.125.227.195:22", "::ffff:169.229.62.97:1473")

# 아래 — 로컬 주소 하나만 bind
ZB = ZA + 4 * STRIDE + 28 + 20
zone(ZB, 3 * STRIDE + 28, "주소 하나만 bind · 10.0.0.1:8888")
y1 = ZB + 32
row(y1 + 0 * STRIDE, "SYN · 10.0.0.1:8888", INFO, "LISTEN", "10.0.0.1:8888", "0.0.0.0:*")
row(y1 + 1 * STRIDE, "데이터 · :16153", MUTED, "ESTABLISHED", "10.0.0.1:8888", "10.0.0.3:16153")
row(y1 + 2 * STRIDE, "SYN · 127.0.0.1:8888", INFO, "RST", "맞는 대기 소켓 없음", "R 0:0(0) ack 591843788", "bad")

d.legend(H - 56, [("새 SYN 을 받는 대기 소켓", ACC), ("연결별 소켓", OK), ("TCP 가 거절", BAD), ("SYN", INFO)])
d.save("13-04.listen-sockets.svg")
