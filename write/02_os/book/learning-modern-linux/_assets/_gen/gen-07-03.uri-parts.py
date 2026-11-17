# 07-03 §2 — URI 다섯 부분과 authority 안의 셋.
# 원문("The Web"): 저자는 부분을 user · password · scheme · authority · path · query · fragment 로 세고
#       authority 를 Hostname("Either as a DNS FQDN or an IP address")과 Port("With a default of 80,
#       so example.com:80 and example.com are the same")로 쪼갠다.
#       user·password — "Initially used for basic authentication, these components should not be used
#       anymore."
#       query·fragment — "The former appears after the ? for nonhierarchical data ..., and the latter
#       appears after the # for secondary resources."
# 2026-11-17: 원서 예시의 순서 정오 상자를 걷어냈다(노트에서 정오 블록을 지움). 도식은 RFC 3986 의
#       바른 순서만 보이고, 대신 서버로 가는 범위(# 앞까지)를 괄호로 표시한다 — RFC 3986 §3.5.
# 타입 스펙: type-nested — 포함 관계로 드러나는 경계. authority 가 userinfo·host·port 를 담는다는
#           사실 자체가 이 절의 논점이라 중첩이 맞다. accent 는 authority.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 534
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §2",
      "사용자 정보는 authority 안에 있고, authority 는 스킴 뒤에 온다",
      "RFC 3986 이 가르는 다섯을 바깥 층으로 두고 그 안에 authority 의 셋을 넣은 것. "
      "서버로 가는 것은 # 앞까지다.",
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
# 서버로 가는 범위 — scheme 부터 query 까지, fragment 는 브라우저에 남는다
SX1 = X0 + 108 + 4 + 352 + 4 + 140 + 4 + 108
BY = Y0 + BH + 52
d.line(X0, BY, SX1, BY, OK, 1.4)
d.line(X0, BY - 6, X0, BY, OK, 1.4)
d.line(SX1, BY - 6, SX1, BY, OK, 1.4)
d.t((X0 + SX1) / 2, BY + 20, "요청에 실려 서버로 가는 범위", 11.5, OK, KR, "middle", 600)
FX0 = SX1 + 4
d.line(FX0, BY, FX0 + 84, BY, MUTED, 1.4)
d.line(FX0, BY - 6, FX0, BY, MUTED, 1.4)
d.line(FX0 + 84, BY - 6, FX0 + 84, BY, MUTED, 1.4)
d.t(FX0 + 42, BY + 20, "브라우저에만", 11.5, MUTED, KR, "middle", 600)

NY = 384
d.tone(X0, NY, 416, 62, WARN)
d.t(X0 + 20, NY + 26, "user:password 형식 — 폐기", 12.5, INK, KR, "start", 600)
d.t(X0 + 20, NY + 48, "RFC 3986 §3.2.1 · 인증은 HTTPS 위 별도 장치로",
    11, MUTED, KR, "start")
d.tone(X0 + 432, NY, 400, 62, OK)
d.t(X0 + 452, NY + 26, "example.com:80 = example.com", 12.5, INK, KR, "start", 600)
d.t(X0 + 452, NY + 48, "http 스킴의 기본 포트 80", 11, MUTED, KR, "start")

d.legend(484, [("스킴", INFO), ("호스트와 포트", OK),
               ("폐기된 형식", WARN), ("authority", ACC)])
d.save("07-03.uri-parts.svg")
print("ok 07-03.uri-parts")
