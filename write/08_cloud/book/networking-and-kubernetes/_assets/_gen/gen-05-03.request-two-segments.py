# 05-03.request-two-segments — 요청 하나가 지나는 두 구간과, 리액트 앱이 실제로 도는 자리
# 본문 요구: 밖에서 들어오는 구간은 주소를 바꾸고(DNAT·SNAT), 컨트롤러에서 백엔드로 가는 구간은
#           주소를 바꾸는 것이 아니라 연결을 새로 연다. 그리고 "리액트 앱이 클러스터에 있다"는 것은
#           정적 파일이 거기서 서빙된다는 뜻이지 코드가 거기서 돈다는 뜻이 아니다.
# 타입 스펙: type-sequence.md — 참여자 넷 사이의 시간순 메시지. 이 폴더의 다른 시퀀스와 같은 ddx.lanes 골격.
#           아래 띠는 시퀀스 문법 밖이라 시간축이 아니라 "어디서 도는가"를 가르는 대조로만 쓴다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 736
d = D(W, H, "REQUEST PATH · TWO SEGMENTS",
      "요청 하나가 성격이 다른 두 구간을 지납니다",
      "밖에서 들어오는 구간은 주소를 바꾸고, 컨트롤러에서 백엔드로 가는 구간은 연결을 새로 연다. "
      "아래 띠는 리액트 앱의 정적 파일과 실행이 서로 다른 자리에 있다는 것을 가른다.",
      lead="주소를 바꾸는 것과 연결을 새로 여는 것은 다른 장치입니다")

LX = ddx.lanes(d, [("브라우저", "클러스터 밖"),
                   ("클러스터 입구", "LoadBalancer 나 NodePort"),
                   ("Ingress 컨트롤러", "프록시 Pod"),
                   ("백엔드 Pod", "앱이 도는 자리")], y0=132, lane_w=212)
RAIL_BOT = 420
for x in LX.values():
    d.line(x, d.lane_top + 4, x, RAIL_BOT, RULE, 1.0, "4 4")

# 클러스터 경계 — 브라우저 레인과 입구 레인 사이
BX = (LX["브라우저"] + LX["클러스터 입구"]) / 2
# 첫 메시지의 라벨이 정확히 이 선 위에 놓인다(경계가 곧 그 메시지의 중점이라). 검사기는
# 글자와 선의 교차를 못 잡으므로 렌더해서 눈으로 찾았고, 선을 두 토막으로 끊어 자리를 비웠다.
d.line(BX, 118, BX, 198, SOFT, 1.2, "8 6")
d.line(BX, 260, BX, RAIL_BOT, SOFT, 1.2, "8 6")
d.t(BX - 12, 112, "클러스터 밖", 11, SOFT, KR, "end")
d.t(BX + 12, 112, "클러스터 안", 11, SOFT, KR, "start")

MSGS = [("브라우저", "클러스터 입구", "GET /", "클러스터 밖에서 들어옵니다", 216, MUTED, None),
        ("클러스터 입구", "Ingress 컨트롤러", "DNAT", "목적지를 컨트롤러 Pod 로", 272, WARN, None),
        ("Ingress 컨트롤러", "백엔드 Pod", "새 연결을 엽니다", "NAT 이 아니라 연결이 둘입니다", 328, ACC, None),
        ("백엔드 Pod", "Ingress 컨트롤러", "응답", "백엔드가 본 출발지는 컨트롤러 Pod", 384, MUTED, "5 4")]
for a, b, lab, sub, y, c, dash in MSGS:
    x1, x2 = LX[a], LX[b]
    dx = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 8 * dx} {y + 12} L {x2 - 12 * dx} {y + 12}", c, 1.6 if c is ACC else 1.5,
           m="acc" if c is ACC else ("warn" if c is WARN else "ar"), dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y, ddx.fit(lab, 12, 224, lab), 12, c, KR)
    d.t(mx, y + 30, ddx.fit(sub, 11, 232, sub), 11, MUTED, KR)

d.t(32, 442, "Cluster 정책이면 첫 구간에서 출발지까지 노드 IP 로 바뀝니다.", 11, MUTED, KR, "start")
d.t(32, 462, "원 클라이언트 IP 는 IP 헤더에 남지 않으므로, 프록시가 X-Forwarded-For 같은 곳에 "
             "따로 적어 넣어야 살아남습니다.", 11, MUTED, KR, "start")

# ── 리액트 앱은 어디에서 도는가
d.line(24, 486, 976, 486, RULE, 0.8)
d.t(32, 514, "리액트 앱은 어디에서 도는가", 13, INK, KR, "start", 600)

d.box(32, 528, 440, 76, PAPER2, RULE, 1.0)
d.t(52, 556, "클러스터가 주는 것", 12, INK, KR, "start", 600)
d.t(52, 578, "index.html 과 번들 JS — 정적 파일입니다", 11, MUTED, KR, "start")

d.tone(528, 528, 440, 76, INFO, 6, "12", 1.2)
d.t(548, 556, "브라우저가 하는 것", 12, INFO, KR, "start", 600)
d.t(548, 578, "그 JS 의 실행 — API 호출도 여기서 출발합니다", 11, MUTED, KR, "start")

d.path("M 478 566 L 522 566", INFO, 1.4, m="info")

d.t(32, 634, "그래서 리액트가 부르는 API 는 클러스터 안에서 나가는 요청이 아니라 맨 윗줄로 다시 "
             "들어오는 요청입니다.", 12, INK, KR, "start")
d.t(32, 656, "서버가 대신 부르는 구성(SSR·BFF)일 때만 Pod 가 직접 부르고, 그때는 Pod 사이 통신입니다. "
             "ClusterIP 를 거치면 그 한 걸음에 DNAT 이 붙습니다.", 11, MUTED, KR, "start")

d.legend(H - 52, [("연결을 새로 여는 구간", ACC), ("주소를 바꾸는 구간", WARN),
                  ("브라우저에서 도는 것", INFO), ("그 밖의 걸음", MUTED)])
d.save("05-03.request-two-segments.svg")
print("ok request-two-segments")
