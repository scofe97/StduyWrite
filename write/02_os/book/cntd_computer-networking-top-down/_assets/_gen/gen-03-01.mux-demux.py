# 03-01 §3 — 원문 3.2 의 상황. 프로세스 넷이 도는 호스트에서 도착한 세그먼트를 어느 소켓에 넣는가.
# 포트 번호는 원문의 예(HTTP 80·FTP 21)와 임의의 임시 포트를 섞었다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 층을 묶고 관계에 포트를 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
PW, PH, PY = 180, 54, 152
XS = [140, 358, 576, 812]
PROCS = [("웹 브라우저", "sock :52410"), ("Zoom", "sock :49918"),
         ("ssh 1", "sock :51002"), ("ssh 2", "sock :51003")]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §3",
      "세그먼트를 어느 소켓에 넣는가",
      "네트워크 층이 호스트까지만 배달한다. 트랜스포트 층이 목적지 포트 번호를 보고 그것을 프로세스의 소켓까지 넓힌다.",
      "이 한 가지가 트랜스포트 층의 최소 업무입니다")

# 애플리케이션 층 zone
d.o.append(f'<rect x="24" y="{PY - 26}" width="{W - 72}" height="{PH + 44}" rx="8" '
           f'fill="{INK}05" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(32, PY - 34, "애플리케이션 층 — 프로세스와 소켓", 11, SOFT, KR, "start")

for x, (name, sock) in zip(XS, PROCS):
    focal = name == "ssh 2"
    if focal:
        d.tone(x - PW / 2, PY, PW, PH, ACC, 6, "14", 1.4)
    else:
        d.box(x - PW / 2, PY, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(x, PY + 24, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x, PY + 43, sock, 11, ACC if focal else SOFT, MONO)

# 트랜스포트 층
TY = 306
d.box(24, TY, W - 72, 60, PAPER2, RULE, 1.0, 6)
d.t(44, TY + 26, "트랜스포트 층", 12, INK, KR, "start", 600)
d.t(44, TY + 46, "목적지 포트 번호로 소켓을 지목합니다 — 역다중화", 11, SOFT, KR, "start")
d.t(W - 68, TY + 36, "UDP · TCP", 11, MUTED, MONO, "end")

# 네트워크 층
NY = 416
d.box(24, NY, W - 72, 60, PAPER2, RULE, 1.0, 6)
d.t(44, NY + 26, "네트워크 층", 12, INK, KR, "start", 600)
d.t(44, NY + 46, "호스트까지만 배달합니다 — 최선 노력", 11, SOFT, KR, "start")
d.t(W - 68, NY + 36, "IP", 11, MUTED, MONO, "end")

# 도착한 세그먼트가 올라가 소켓으로 갈라진다
d.path(f"M 120 {NY} L 120 {TY + 60}", MUTED, 1.4, m="ar")
d.t(132, (NY + TY + 60) / 2 + 4, "도착한 세그먼트", 11, SOFT, KR, "start")
for x, (name, sock) in zip(XS, PROCS):
    c = ACC if name == "ssh 2" else MUTED
    d.path(f"M {x} {TY} L {x} {PY + PH + 10}", c, 1.3, m="acc" if c is ACC else "ar")
d.t(XS[3] + 8, (TY + PY + PH) / 2 + 4, "목적지 포트 51003", 11, ACC, KR, "start")

d.t(24, 518, "다중화는 반대 방향입니다. 여러 소켓의 데이터를 모아 헤더를 붙이고 세그먼트를 만들어 네트워크 층으로 내립니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("이 세그먼트가 갈 자리", ACC), ("다른 소켓", MUTED)])
d.save("03-01.mux-demux.svg")
