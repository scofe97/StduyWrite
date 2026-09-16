# 05-03.request-two-segments — 요청 하나가 지나는 두 구간
# 본문 요구: 밖에서 들어오는 구간은 주소를 바꾸고(DNAT·SNAT), 컨트롤러에서 백엔드로 가는 구간은
#           주소를 바꾸는 것이 아니라 연결을 새로 연다.
# 타입 스펙: type-sequence.md — 참여자 넷 사이의 시간순 메시지. 이 폴더의 다른 시퀀스와 같은 ddx.lanes 골격.
# 이력: 2026-09-16 한 장에 주제가 둘이라 아래 띠("리액트 앱은 어디에서 도는가")를 떼어
#       gen-05-03.react-runs-in-browser.py 로 옮겼다. 시간축 밖 대조가 시퀀스에 섞여 있던 자리다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 520
d = D(W, H, "REQUEST PATH · TWO SEGMENTS",
      "요청 하나가 성격이 다른 두 구간을 지납니다",
      "밖에서 들어오는 구간은 주소를 바꾸고, 컨트롤러에서 백엔드로 가는 구간은 연결을 새로 연다. "
      "브라우저에서 클러스터 입구, 컨트롤러, 백엔드 Pod 로 이어지는 네 레인의 시간순 메시지로 그렸다.",
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

MSGS = [("브라우저", "클러스터 입구", "GET /", "클러스터 밖에서 진입", 216, MUTED, None),
        ("클러스터 입구", "Ingress 컨트롤러", "DNAT", "목적지를 컨트롤러 Pod 로", 272, WARN, None),
        ("Ingress 컨트롤러", "백엔드 Pod", "새 연결", "NAT 아님 · 연결 둘", 328, ACC, None),
        ("백엔드 Pod", "Ingress 컨트롤러", "응답", "백엔드가 본 출발지 · 컨트롤러 Pod", 384, MUTED, "5 4")]
for a, b, lab, sub, y, c, dash in MSGS:
    x1, x2 = LX[a], LX[b]
    dx = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 8 * dx} {y + 12} L {x2 - 12 * dx} {y + 12}", c, 1.6 if c is ACC else 1.5,
           m="acc" if c is ACC else ("warn" if c is WARN else "ar"), dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y, ddx.fit(lab, 12, 224, lab), 12, c, KR)
    d.t(mx, y + 30, ddx.fit(sub, 12, 232, sub), 12, MUTED, KR)


d.legend(H - 52, [("연결을 새로 여는 구간", ACC), ("주소를 바꾸는 구간", WARN),
                  ("그 밖의 걸음", MUTED)])
d.save("05-03.request-two-segments.svg")
print("ok request-two-segments")
