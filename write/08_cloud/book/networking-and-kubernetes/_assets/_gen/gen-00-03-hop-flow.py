# 00-03-hop-flow — 구간마다 무엇이 다시 쓰이는가
# 본문 요구: "값 아래가 그 주소의 주인이다. 세 줄 중 마지막 줄만 처음부터 끝까지 같은 값이다."
#           NAT 이 일어나는 가운데 구간이 초점이다.
# 타입 스펙: type-process.md — 구간마다 DST MAC · SRC IP · DST IP 라는 같은 의미 슬롯이 반복되고,
#           구간 간 비교가 메시지 타이밍보다 중요하다. semantic-patterns.md 의
#           "Stage framework with semantic slots" 가 이 형태를 process 로 보낸다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 596
DEV_Y, DEV_W, DEV_H, DEV_STRIDE = 132, 170, 76, 240
SEG_X0, SEG_W, SEG_Y, SEG_H, SEG_STRIDE = 165, 200, 256, 232, 240
DEVICES = [("내 노트북", "192.168.0.15"), ("집 공유기", "NAT 이 여기서"),
           ("ISP 라우터", "중간 홉"), ("웹 서버", "93.184.216.34")]
# 구간마다 같은 슬롯 셋 — (값, 주인, 색). 가운데 구간만 focal.
SEGMENTS = [
    (False, [("AA:BB:CC:00:00:02", "공유기 LAN 쪽", INFO, MUTED),
             ("192.168.0.15", "내 노트북", WARN, MUTED),
             ("93.184.216.34", "웹 서버", OK, MUTED)]),
    (True,  [("AA:BB:CC:00:00:03", "ISP 라우터", INFO, MUTED),
             ("203.0.113.7", "공유기 공인 · NAT", WARN, ACC),
             ("93.184.216.34", "웹 서버", OK, MUTED)]),
    (False, [("AA:BB:CC:00:00:04", "웹 서버 NIC", INFO, MUTED),
             ("203.0.113.7", "공유기 공인", WARN, MUTED),
             ("93.184.216.34", "웹 서버", OK, MUTED)]),
]
SLOTS = ["DST MAC", "SRC IP", "DST IP"]

d = D(W, H, "PROCESS · WHAT GETS REWRITTEN",
      "구간마다 무엇이 다시 쓰이는가",
      "장비 넷을 가로로 잇고 구간마다 목적지 MAC 과 출발지·목적지 IP 를 값과 그 주인 이름까지 붙인 흐름도. "
      "MAC 은 세 번, 출발지 IP 는 NAT 에서 한 번 바뀌고 목적지 IP 만 끝까지 같다.",
      lead="값 아래가 그 주소의 주인입니다. 세 줄 중 마지막 줄만 처음부터 끝까지 같은 값입니다.")

for i, (name, sub) in enumerate(DEVICES):
    x = 60 + i * DEV_STRIDE
    d.box(x, DEV_Y, DEV_W, DEV_H, PAPER2, RULE, 1.0, 6)
    d.t(x + DEV_W // 2, DEV_Y + 32, name, 14, INK, KR, "middle", 600)
    d.t(x + DEV_W // 2, DEV_Y + 54, sub, 11, MUTED,
        MONO if all(ord(c) < 128 or c == '.' for c in sub) else KR)
    if i < 3:
        d.path(f"M {x + DEV_W} {DEV_Y + 38} L {x + DEV_STRIDE - 8} {DEV_Y + 38}", MUTED, 1.4, m="ar")

for i, (focal, slots) in enumerate(SEGMENTS):
    x = SEG_X0 + i * SEG_STRIDE
    if focal:
        d.tone(x, SEG_Y, SEG_W, SEG_H, ACC, 8, "12", 1.2)
    else:
        d.box(x, SEG_Y, SEG_W, SEG_H, PAPER2, RULE, 1.0, 8)
    for j, ((val, who, vc, wc), slot) in enumerate(zip(slots, SLOTS)):
        y = SEG_Y + 24 + j * 76
        d.t(x + 16, y, slot, 8, SOFT, MONO, "start")
        d.t(x + 16, y + 20, val, 11, vc, MONO, "start")
        d.t(x + 16, y + 42, who, 12, wc, KR, "start")

d.t(60, 512, "구간이 바뀔 때마다 겉봉은 새로 쓰이지만, 어디로 가는지는 처음 적힌 값이 그대로 갑니다.",
    12, MUTED, KR, "start")
d.legend(528, [("MAC · 구간마다 새로", INFO), ("출발지 IP · NAT 에서 한 번", WARN),
               ("목적지 IP · 끝까지 그대로", OK)])
d.save("00-03-hop-flow.svg")
print("ok hop-flow")
