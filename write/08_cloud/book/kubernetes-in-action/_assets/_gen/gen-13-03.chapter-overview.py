# 13-03 전체 지도 — 네 축은 순서가 아니다
# 본문이 "순서대로 이어지는 파이프라인이 아니라 각각 독립된 주제"라고 못박으므로 체인으로
# 그리면 안 된다. 관통 질문("무엇을 아는가")을 사다리로 세우고 네 축은 그 아래 나란히 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 13-03",
      "게이트웨이가 무엇을 아는가",
      "네 주제를 관통하는 질문은 하나다. 아는 것이 많을수록 라우팅할 수 있는 범위가 넓어지고, "
      "모를수록 조건 없이 전달하는 데 그친다.",
      "HTTP 를 넘어 TLS · 기타 프로토콜 · 네임스페이스 · mesh 로")

ddx.band(d, 100, 316, "아는 것의 사다리", x=24, w=1192, focal=True)
RUNG = [("안의 HTTP 까지 안다", "TLS 를 직접 종료했다", "경로 · 헤더 · 쿠키로 가른다", OK),
        ("SNI 호스트명만 안다", "통과시켰다", "호스트로만 가른다", WARN),
        ("아무것도 모른다", "TCP · UDP", "조건 없이 전달한다", SOFT)]
for i, (t, why, can, c) in enumerate(RUNG):
    cx = 240 + i * 380
    d.box(cx - 170, 158, 340, 128, PAPER2, c, 1.1, 6)
    d.t(cx, 190, t, 13, c, KR, "middle", 600)
    d.t(cx, 216, why, 11, MUTED, KR)
    d.t(cx, 252, can, 11, SOFT, KR)
    if i < 2:
        d.path(f"M {cx+176} 222 L {cx+198} 222", MUTED, 1.4, m="ar")
d.t(620, 306, "왼쪽으로 갈수록 할 수 있는 일이 많아진다", 11, ACC, KR)

AXIS = [("§1  TLS", "termination 이냐 passthrough 냐"),
        ("§2  기타 프로토콜", "TCP · UDP · gRPC 도 Route 로"),
        ("§3  크로스 네임스페이스", "참조에는 허가가 따로 필요하다"),
        ("§4  mesh", "north/south 에서 east/west 로")]
d.t(24, 366, "네 축 — 순서가 아니라 각각 독립된 주제다", 12, SOFT, KR, "start")
for i, (t, s) in enumerate(AXIS):
    cx = 176 + i * 296
    d.box(cx - 136, 386, 272, 84, PAPER2, INFO, 1.1, 6)
    d.t(cx, 418, t, 13, INFO, KR, "middle", 600)
    d.t(cx, 442, ddx.fit(s, 11, 252, s), 11, MUTED, KR)

d.t(24, 522, "TLS 를 직접 종료하면 안이 HTTP 임을 알아 경로·헤더까지 본다. 통과시키면 SNI 호스트명만 남고, "
             "TCP 에서는 그마저 없다.", 11, MUTED, KR, "start")
d.legend(548, [("아는 것이 많다", OK), ("호스트만", WARN), ("네 축", INFO)])
d.save("13-03.chapter-overview.svg")
print("ok")
