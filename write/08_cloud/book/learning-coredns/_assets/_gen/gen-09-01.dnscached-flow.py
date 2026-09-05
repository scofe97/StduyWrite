# 09-01 §7 — 플래그가 구조체를 거쳐 Corefile 문자열이 되어 Caddy 에 들어간다.
# 원문 근거: main 의 흐름 넷 — "1. Parse the flags, creating a dnscached struct ... 2. Use that
#            struct to generate the Corefile in memory. 3. Start up the server with that Corefile.
#            4. Simply wait for the server to exit" / "Although it is technically possible to
#            construct a server directly in code, it is not easy and would repeat a lot of Caddy
#            code. Feeding a string version of a Corefile to Caddy ... is much simpler."
# 타입 스펙: type-process — 단계가 순서대로 이어지고 각 단계의 산출물이 다음 단계의 입력이다.
#           문자열을 거치는 우회가 왜 지름길인지가 이 흐름에서만 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 546
d = D(W, H, "LEARNING COREDNS · 09-01 §7",
      "플래그가 구조체를 거쳐 Corefile 문자열이 되기까지",
      "자기 main 은 서버를 코드로 조립하지 않는다. 플래그를 구조체에 모아 Corefile 문자열을 "
      "만들고 그것을 Caddy 에 먹인다.",
      "주황이 코드 대신 문자열을 거치는 자리입니다")

CW, CG, X0, CY, CH = 190, 24, 30, 150, 96
XS = [X0 + i * (CW + CG) for i in range(4)]
CARDS = [
    ("01", "플래그를 파싱한다", "새 flag.FlagSet 으로", "import 한 플래그를 배제"),
    ("02", "구조체에 모은다", "dnscached struct", "전역 변수를 쓰지 않는다"),
    ("03", "Corefile 을 짓는다", "bytes.Buffer 에 쓴다", "-dry-run 으로 볼 수 있다"),
    ("04", "Caddy 에 먹인다", "caddy.Start(input)", "ServerTypeName: \"dns\""),
]

for i in range(3):
    d.arrow([(XS[i] + CW, CY + CH / 2), (XS[i + 1] - 2, CY + CH / 2)], MUTED, "ar", 1.4)

for i, (n, t1, t2, t3) in enumerate(CARDS):
    x = XS[i]
    if i == 2:
        d.tone(x, CY, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, CY + 26, n, 11, ACC if i == 2 else SOFT, MONO, "start", 600)
    d.t(x + 16, CY + 52, t1, 14, ACC if i == 2 else INK, KR, "start", 600)
    d.t(x + 16, CY + 74, t2, 11, MUTED, MONO, "start")
    d.t(x + 16, CY + 92, t3, 11, MUTED, KR, "start")

d.arrow([(XS[3] + CW / 2, CY + CH), (XS[3] + CW / 2, 300)], MUTED, "ar", 1.4)
d.box(XS[3] - 15, 302, CW + 30, 56, PAPER2, RULE, 1.0)
d.t(XS[3] + CW / 2, 326, "instance.Wait()", 13, INK, MONO, "middle", 600)
d.t(XS[3] + CW / 2, 346, "시그널 처리를 넣지 않는 한 안 돌아온다", 11, MUTED, KR)

d.tone(30, 302, 420, 56, ACC, 6, "0E", 1.3)
d.t(240, 326, "왜 문자열을 거치는가", 13, ACC, KR, "middle", 600)
d.t(240, 346, "코드로 서버를 짓는 것도 되지만 Caddy 코드를 많이 반복하게 된다", 11, MUTED, KR)

d.box(20, 382, 840, 84, PAPER, RULE, 0.8)
d.t(36, 406, "이 길에서 얻는 것", 12, INK, KR, "start", 600)
d.t(36, 430, "필요한 플러그인만 이름 없는 import 로 골라 바이너리를 줄인다", 11, MUTED, KR, "start")
d.t(36, 452, "자기 플래그를 받고 이름도 coredns 가 아닌 것으로 지을 수 있다", 11, MUTED, KR, "start")

d.legend(486, [("코드 대신 문자열을 거치는 자리", ACC)])
d.save("09-01.dnscached-flow.svg")
