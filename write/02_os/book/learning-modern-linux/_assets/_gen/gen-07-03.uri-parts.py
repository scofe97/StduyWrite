# 07-03 §2 — URI 다섯 부분과 authority 안의 셋.
# 원문("The Web"): 저자는 부분을 user · password · scheme · authority · path · query · fragment 로 세고
#       authority 를 Hostname("Either as a DNS FQDN or an IP address")과 Port("With a default of 80,
#       so example.com:80 and example.com are the same")로 쪼갠다.
#       user·password — "Initially used for basic authentication, these components should not be used
#       anymore."
#       query·fragment — "The former appears after the ? for nonhierarchical data ..., and the latter
#       appears after the # for secondary resources."
# 주의: 원문의 예시 문자열은 michaelh:12345678@http://example.com:4242/... 로 스킴 앞에 사용자 정보를
#       둔다. RFC 3986 §3 은 URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ] 이고
#       §3.2 는 authority = [ userinfo "@" ] host [ ":" port ] 이므로 순서가 뒤집혔다. 도식은 RFC 의
#       다섯을 바깥 층으로 두고 authority 안에 셋을 넣어, 원문이 어디에서 어긋났는지가 보이게 한다.
# 타입 스펙: type-nested — 포함 관계로 드러나는 경계. authority 가 userinfo·host·port 를 담는다는
#           사실 자체가 이 절의 논점이라 중첩이 맞다. accent 는 순서가 뒤집힌 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 596
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §2",
      "사용자 정보는 authority 안에 있고, authority 는 스킴 뒤에 온다",
      "RFC 3986 이 가르는 다섯을 바깥 층으로 두고 그 안에 authority 의 셋을 넣은 것. "
      "원서의 예시는 사용자 정보를 스킴 앞에 두어 순서가 뒤집혀 있다.",
      "포트 80 은 기본값이라 생략할 수 있습니다")

Y0, BH = 164, 96
parts = [
    ("scheme", "http", 108, INFO),
    ("authority", "michaelh:12345678@example.com:4242", 352, ACC),
    ("path", "/this/is/the/way", 140, OK),
    ("query", "?orisit=really", 108, MUTED),
    ("fragment", "#anchor", 84, MUTED),
]
X0 = 24
GAP = 4
x = X0
for name, val, w, col in parts:
    focal = (col is ACC)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y0}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(x, Y0, w, BH, PAPER2, col, 1.2, 6)
    d.t(x + w / 2, Y0 + 24, name, 12.5, col, KR, "middle", 600)
    if w >= 108:
        d.t(x + w / 2, Y0 + 48, val, 11, INK, MONO)
    else:
        d.t(x + w / 2, Y0 + 48, val, 10, INK, MONO)
    x += w + GAP

# authority 안쪽 셋
AX = X0 + parts[0][2] + GAP
AW = parts[1][2]
inner = [("userinfo", "michaelh:12345678", 150, WARN),
         ("host", "example.com", 112, OK),
         ("port", ":4242", 58, OK)]
ix = AX + 8
for name, val, w, col in inner:
    d.o.append(f'<rect x="{ix}" y="{Y0 + 58}" width="{w}" height="34" rx="4" '
               f'fill="{col}18" stroke="{col}" stroke-width="1.1"/>')
    d.t(ix + w / 2, Y0 + 73, name, 10.5, col, KR, "middle", 600)
    d.t(ix + w / 2, Y0 + 87, val, 9, MUTED, MONO)
    ix += w + 4

d.t(X0, Y0 + BH + 26, "http://michaelh:12345678@example.com:4242/this/is/the/way?orisit=really#anchor",
    12.5, INK, MONO, "start")
d.t(X0, Y0 + BH + 46, "RFC 3986 대로 세우면 이렇습니다", 11.5, OK, KR, "start")

WY = 344
d.tone(X0, WY, W - 48, 96, WARN)
d.t(X0 + 20, WY + 28, "원문 정오 — 순서가 뒤집혀 있습니다", 13, INK, KR, "start", 600)
d.t(X0 + 20, WY + 52, "원서의 예시는 michaelh:12345678@http://example.com:4242/... 입니다.",
    11.5, MUTED, MONO, "start")
d.t(X0 + 20, WY + 74,
    "RFC 3986 은 URI = scheme \":\" hier-part 이고 authority = [ userinfo \"@\" ] host [ \":\" port ] 입니다.",
    11.5, MUTED, MONO, "start")

NY = 460
d.tone(X0, NY, 416, 62, INFO)
d.t(X0 + 20, NY + 26, "user 와 password 는 쓰지 말아야 합니다", 12.5, INK, KR, "start", 600)
d.t(X0 + 20, NY + 48, "기본 인증에 쓰이던 것이라 지금은 HTTPS 와 제대로 된 인증을 씁니다.",
    11, MUTED, KR, "start")
d.tone(X0 + 432, NY, 400, 62, OK)
d.t(X0 + 452, NY + 26, "example.com:80 과 example.com 은 같습니다", 12.5, INK, KR, "start", 600)
d.t(X0 + 452, NY + 48, "http 스킴의 기본 포트가 80 이기 때문입니다.", 11, MUTED, KR, "start")

d.legend(552, [("스킴", INFO), ("호스트와 포트", OK),
               ("쓰지 말아야 할 부분", WARN), ("순서가 어긋난 자리", ACC)])
d.save("07-03.uri-parts.svg")
print("ok 07-03.uri-parts")
