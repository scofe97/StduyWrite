# 04-04.response-signatures — 같은 정책 하나가 만드는 응답 서명 셋
# 본문 요구: `## Cilium L7 정책` 의 확인된 것 — demo 의 GET / 는 200(nginx 까지), GET /health 는 403(Access denied · content-length 15 · server: envoy, 프록시까지만),
#           cart 는 000(3.00s 타임아웃, 출발지 판정에서 커널이 버림). 넓은 표준 정책을 옆에 두면 /health 가 404(nginx)로 바뀌어 L7 제약이 사라진다.
# 타입 스펙: type-architecture — 존으로 묶은 노드 그래프. 세 요청이 어느 존(커널 · Envoy · nginx)에서 멈추는지가 논지라
#           존을 세로 띠로 두고 요청마다 한 줄씩 화살표를 보낸다. coral focal 은 프록시에서 끝나는 403 줄 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 600


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 04-04 RESPONSE SIGNATURES",
      "응답 코드는 어디서 멈췄는지를 알려 줍니다",
      "Cilium L7 정책 하나가 만드는 응답 서명 셋. cart 의 GET / 는 출발지 목록에 없어 커널에서 버려져 000 과 3.00초 타임아웃이 된다. "
      "demo 의 GET /health 는 Envoy 까지 가서 Access denied 와 403 을 받는다. demo 의 GET / 는 nginx 까지 가서 200 을 받는다. "
      "넓은 표준 정책을 옆에 두면 /health 는 404 로 바뀐다.",
      lead="화살표가 멈춘 존이 곧 서명입니다")

SX, SW = 24, 152
ZX = [(206, 180), (402, 180), (598, 180)]
GX, GW = 806, 170
ZONES = [("커널", "출발지 판정 · L3 L4"), ("Envoy", "경로 판정 · L7"), ("nginx", "demo-db 서버")]
RYS = [250, 350, 450]
Y_TOP, Y_BOT = 122, 500

for (x, w), (h1, h2) in zip(ZX, ZONES):
    d.box(x, Y_TOP + 10, w, Y_BOT - Y_TOP - 10, PAPER2, RULE, 0.9, 8)
    d.t(x + w / 2, Y_TOP + 34, h1, 14, INK, kr(h1), "middle", 600)
    d.t(x + w / 2, Y_TOP + 54, ddx.fit(h2, 12, w - 12, h2), 12, MUTED, kr(h2), "middle")
d.t(GX + GW / 2, Y_TOP + 34, "받은 서명", 14, INK, KR, "middle", 600)
d.t(SX + SW / 2, Y_TOP + 34, "요청", 14, INK, KR, "middle", 600)

ROWS = [
    # 출발, 요청, 멈춘 존 인덱스, 존 안 설명, 서명 코드, 서명 부제, 색
    ("cart", "GET /", 0, "목록에 없음 → 버림", "000", "3.00s 타임아웃", BAD),
    ("demo", "GET /health", 1, "정책에 없는 경로 → 거절", "403", "Access denied · envoy", ACC),
    ("demo", "GET /", 2, "경로 허용 → 서버로", "200", "nginx 응답", OK),
]

for (src, req, z, note, code, sub, c), y in zip(ROWS, RYS):
    d.box(SX, y - 28, SW, 56, PAPER2, RULE, 1.0, 6)
    d.t(SX + 16, y - 4, src, 13, INK, MONO, "start", 600)
    d.t(SX + 16, y + 17, req, 12, MUTED, MONO, "start")

    zx, zw = ZX[z]
    stop = zx + zw / 2
    d.arrow([(SX + SW + 2, y), (stop - 8, y)], c if c == ACC else MUTED, "acc" if c == ACC else "ar", 1.6)
    if c == BAD:
        for sgn in (1, -1):
            d.line(stop - 6, y - 7 * sgn, stop + 8, y + 7 * sgn, BAD, 2.0)
    d.t(stop, y - 14, ddx.fit(note, 12, zw - 12, note), 12, c if c != OK else MUTED, kr(note), "middle", 600 if c == ACC else 400)

    d.line(stop + 14, y, GX - 6, y, SOFT, 1.0, "4 4")
    if c == ACC:
        d.tone(GX, y - 32, GW, 64, ACC, 8, "1F", 1.6)
    else:
        d.tone(GX, y - 32, GW, 64, c, 8, "14", 1.1)
    d.t(GX + GW / 2, y - 2, code, 20, c, MONO, "middle", 600)
    d.t(GX + GW / 2, y + 21, ddx.fit(sub, 12, GW - 12, sub), 12, MUTED, kr(sub), "middle")

d.t(24, 528, "넓은 표준 정책을 옆에 두면 /health 403 → 404 (nginx 응답 · L7 제약 사라짐)", 12, MUTED, KR, "start")
d.legend(548, [("서버까지 간 응답", OK), ("출발지 판정에서 버려짐", BAD), ("프록시에서 끝난 응답", ACC)])
d.save("04-04.response-signatures.svg")
print("ok response-signatures")
