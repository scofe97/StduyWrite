# 03-03.same-host-access — 같은 호스트인데 컨테이너마다 스택이 따로다
# 본문 요구: 매핑은 호스트 스택에만 있고, 컨테이너 안에서는 컨테이너 포트만 열린다.
#           컨테이너끼리는 자기 lo 가 자기 것이라 서로 안 통한다.
# 타입 스펙: type-nested.md 경계 링 + 두 끝점. 서로 안 통한다는 사실이 요점이라
#           그 끊긴 자리에 focal 을 건다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 604
d = D(W, H, "SAME HOST · SEPARATE STACKS",
      "같은 호스트 안 — 컨테이너마다 자기 스택을 따로 가진다",
      "매핑은 호스트 스택에만 있다. 컨테이너 안에서는 컨테이너 포트만 열려 있고, 자기 lo 는 자기 것이라 서로 닿지 않는다.",
      lead="매핑은 호스트 스택에만 있고, 자기 lo 는 자기 것이라 서로 닿지 않는다")

BW, BH = 208, 104
HOST = (146, 346)
RING = (300, 216, 660, 300)
D0, WEB, DNS = (438, 346), (768, 276), (768, 416)

def box(cx, cy, t, s, tag, c=None, w=BW):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 20, ddx.fit(t, 13, w - 18, t), 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(s, 11, w - 16, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':.' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 556, "밖에서 두드릴 때 쓰는 포트와 안에서 열려 있는 포트가 다르다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "컨테이너 네트워크 172.17.0.0/16 — 안에서는 컨테이너 포트만", 11, INFO, off=16)

box(*HOST, "호스트 스택", "127.0.0.1:80", "매핑은 여기에만 있다", WARN)
box(*D0, "docker0", "172.17.0.1", "매핑 80 → 8080")
box(*WEB, "go-web", "172.17.0.2:8080", "8080 은 여기서만 열림", OK)
box(*DNS, "dnsutils", "dnsutils:1.3 이미지", "자기 lo 는 자기 것")

d.path(f"M {HOST[0]+BW//2+6} {HOST[1]} L {D0[0]-BW//2-10} {D0[1]}", MUTED, 1.5, m="ar")
d.t((HOST[0] + D0[0]) // 2, HOST[1] - 16, "호스트 포트 80", 10, MUTED, KR)
for t in (WEB, DNS):
    d.path(f"M {D0[0]+BW//2+6} {D0[1] + (t[1]-D0[1])//4} L {t[0]-BW//2-10} {t[1]}", MUTED, 1.4, m="ar")

# 두 컨테이너는 서로의 lo 에 닿지 않는다 — 이 도식의 focal
# 두 박스 사이 좁은 틈에 태그를 두면 양쪽을 덮는다 — 선만 긋고 라벨은 왼쪽 코리도어에
BY = (WEB[1] + DNS[1]) // 2
d.line(WEB[0] - BW // 2, BY, WEB[0] + BW // 2, BY, BAD, 1.6, "6 5")
d.o.append(f'<line x1="{WEB[0]-14}" y1="{BY-12}" x2="{WEB[0]+14}" y2="{BY+12}" '
           f'stroke="{BAD}" stroke-width="2.4"/>')
d.o.append(f'<line x1="{WEB[0]-14}" y1="{BY+12}" x2="{WEB[0]+14}" y2="{BY-12}" '
           f'stroke="{BAD}" stroke-width="2.4"/>')
d.t(WEB[0] - BW // 2 - 12, BY + 4, "lo 로는 안 통한다", 11, BAD, KR, "end")

d.t(36, 528, "각자 별개 스택이라 127.0.0.1 이 서로 다른 곳을 가리킨다 — 한 묶음으로 묶어야 "
             "그 주소를 공유하게 되고, 그것이 Pod 다", 12, MUTED, KR, "start")
d.legend(572, [("호스트 쪽", WARN), ("컨테이너 네트워크", INFO), ("서로 안 통한다", BAD)])
d.save("03-03.same-host-access.svg")
print("ok same-host-access")
