# 05-03 §Envoy 사이드카 — 한 네트워크 네임스페이스에 포트가 셋 선다
# 본문: Node.js 는 HTTP 를 직접 받고, Envoy 가 HTTPS(8443)·admin(9901)을 받아 loopback 으로
#       Node.js 에 HTTP 로 넘긴다. 두 컨테이너가 같은 네트워크 네임스페이스를 쓴다(05-01 §3).
# 타입 스펙: type-nested.md — Pod 라는 경계 안에 인터페이스 둘과 컨테이너 둘이 든 그림이다.
#           포트가 어느 인터페이스에 서는지가 요점이므로 인터페이스를 축으로 삼는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 596
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "포트 셋이 한 네트워크 네임스페이스에 함께 선다",
      "Envoy 가 밖에서 오는 HTTPS(8443)와 admin(9901)을 받고, Node.js 는 HTTP(8080)를 받는다. "
      "같은 네임스페이스를 쓰므로 Envoy 는 loopback 으로 Node.js 에 넘길 수 있다.",
      lead="포트 공간이 하나라서 셋이 겹치면 안 된다 — 05-01 §3 의 공유가 여기서 값과 대가를 함께 낸다")

RING = (60, 200, 880, 268)
ETH, LO = (250, 268), (250, 396)
ENVOY, NODE = (700, 268), (700, 396)
BW, BH = 300, 92

ddx.band(d, 104, 540, "밖에서 오는 것은 eth0 로, 안에서 건네는 것은 lo 로 간다")

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "kiada-ssl Pod — 두 컨테이너가 같은 네트워크 네임스페이스", 11, INFO, off=16)

def box(cx, cy, t, s, tag, c):
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 20, ddx.fit(t, 13, BW - 18, t), 13, c,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, BW - 16, t), 11, MUTED, MONO)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, t), 10, SOFT, KR)

box(*ETH, "eth0", "8443 · 9901 · 8080", "밖에서 들어오는 인터페이스", WARN)
box(*LO, "lo  127.0.0.1", "8080", "안에서만 쓰는 인터페이스", ACC)
box(*ENVOY, "Envoy 사이드카", "8443 HTTPS · 9901 admin", "밖의 HTTPS 를 받는다", OK)
box(*NODE, "kiada (Node.js)", "8080 HTTP", "두 인터페이스의 8080 에 바인딩", INFO)

d.path(f"M {ETH[0]+BW//2+6} {ETH[1]} L {ENVOY[0]-BW//2-10} {ENVOY[1]}", WARN, 1.6, m="warn")
d.chip(475, ETH[1], "HTTPS · admin", WARN, 11)
d.path(f"M {LO[0]+BW//2+6} {LO[1]} L {NODE[0]-BW//2-10} {NODE[1]}", ACC, 1.6, m="acc")
d.chip(475, LO[1], "평문 HTTP", ACC, 11)
d.path(f"M {ENVOY[0]} {ENVOY[1]+BH//2+6} L {ENVOY[0]} {NODE[1]-BH//2-10}", ACC, 1.6, m="acc")
d.t(860, 332, "Envoy 가 lo 로 넘긴다", 11, ACC, KR)

d.t(36, 500, "Node.js 는 두 인터페이스의 8080 에 모두 바인딩돼 있어, 밖에서 온 HTTP 도 Envoy 가 "
             "넘긴 HTTP 도 같은 포트로 받는다", 12, MUTED, KR, "start")
d.legend(556, [("Pod 경계와 HTTP 만 아는 앱", INFO), ("밖에서 들어오는 길", WARN),
               ("안에서 건네는 길", ACC), ("HTTPS 를 대신 받는 쪽", OK)])
d.save("05-03-envoy-sidecar-network.svg")
print("ok envoy-sidecar-network")
