# 05-03 §TLS 종료 — 앱 코드 0줄로 HTTPS 가 된다
# 본문: "kiada 앱은 HTTP 만 안다. Envoy 를 옆에 붙인 것만으로 HTTPS 가 된다 — 앱 코드 0줄 수정."
#       실측: 8080(HTTP)과 8443(HTTPS)이 완전히 같은 응답. Client IP=127.0.0.1 →
#       앱에는 자기 Pod 안 Envoy 가 localhost 로 넘긴 것으로 보인다.
# 타입 스펙: type-architecture.md — 세 칸 한 줄 사슬 + 되돌아오는 응답. 어디서 암호가 풀리는지가 요점이므로
#           그 경계(TLS 종료)를 Envoy 상자 위에 못 박는다.
#           Pod 경계가 점선 영역이고 그 안에 Envoy 와 앱을 위아래로 둔 뒤 왕복 세 화살표를 잇는다.
#           암호가 풀리는 경계가 영역 안이라는 사실이 논지라 경계와 흐름을 함께 그리는 형태여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 620
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "TLS 는 Envoy 에서 끝나고, 앱은 평문만 본다",
      "Envoy 가 8443 에서 HTTPS 를 받아 암호를 풀고 평문 HTTP 로 localhost:8080 에 넘긴다. "
      "kiada 는 HTTPS 를 받았다는 사실조차 모르고, 코드는 한 줄도 바뀌지 않는다.",
      lead="실측에서 8080 과 8443 의 응답이 완전히 같았다 — 앱이 보는 Client IP 는 127.0.0.1 이다")

# 두 컨테이너를 나란히 두면 사이 통로가 30px 뿐이라 ②③ 칩이 상자를 덮는다(chip error).
# 위아래로 쌓으면 그 사이가 52px 열리고, 왕복 두 방향을 서로 다른 열에 세울 수 있다.
RING = (300, 190, 660, 300)
CLIENT = (140, 300)
ENVOY, NODE = (630, 268), (630, 412)
BW, BH = 380, 108

ddx.band(d, 104, 564, "암호가 풀리는 자리가 Pod 안이라, 앱에는 자기 Pod 안에서 온 평문으로 보인다")

def box(cx, cy, t, s, tag, c, w=BW):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 24, ddx.fit(t, 13, w - 18, t), 13, c, KR, "middle", 600)
    d.t(cx, cy, ddx.fit(s, 11, w - 16, t), 11, MUTED, MONO)
    d.t(cx, cy + 24, ddx.fit(tag, 10, w - 14, t), 10, SOFT, KR)

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "kiada-ssl Pod — localhost 를 공유한다", 11, INFO, off=16)

box(*CLIENT, "클라이언트", "curl -k https://:8443", "밖에서 온다", MUTED, w=200)
box(*ENVOY, "Envoy 사이드카", "8443 HTTPS → 암호 해제", "여기서 TLS 가 끝난다", ACC)
box(*NODE, "kiada (Node.js)", "8080 · 평문만 안다", "HTTPS 였다는 걸 모른다", INFO)

d.path(f"M {CLIENT[0]+100+6} {CLIENT[1]} L 360 {CLIENT[1]} L 360 {ENVOY[1]} "
       f"L {ENVOY[0]-BW//2-10} {ENVOY[1]}", WARN, 1.8, m="warn")
d.chip(360, 284, "① HTTPS", WARN, 11)
d.path(f"M {ENVOY[0]-60} {ENVOY[1]+BH//2+6} L {NODE[0]-60} {NODE[1]-BH//2-10}", ACC, 1.8, m="acc")
d.chip(ENVOY[0] - 60, 340, "② 평문", ACC, 11)
d.path(f"M {NODE[0]+60} {NODE[1]-BH//2-6} L {ENVOY[0]+60} {ENVOY[1]+BH//2+10}", INFO, 1.6, m="info")
d.chip(ENVOY[0] + 60, 340, "③ 평문 응답", INFO, 11)

# Pod 링이 y 490 까지 내려온다 — 산문은 그 아래로
d.t(36, 512, "앱이 보는 Client IP 는 127.0.0.1 이다 — 같은 Pod 안 Envoy 가 localhost 로 넘겼기 때문이다.",
     12, MUTED, KR, "start")
d.t(36, 536, "레거시 앱에 HTTPS 를 붙이는 표준 수단이 이것이다 — 붙이는 것은 프로세스 하나뿐이다.",
     12, MUTED, KR, "start")
d.legend(580, [("암호화된 구간", WARN), ("TLS 가 끝나는 자리와 평문 구간", ACC),
               ("Pod 경계와 평문만 아는 앱", INFO)])
d.save("05-03-envoy-tls-termination.svg")
print("ok envoy-tls-termination")
