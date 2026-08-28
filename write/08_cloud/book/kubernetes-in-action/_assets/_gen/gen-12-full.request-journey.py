# 12장 마무리 — 두 줄이 만나지 않는다
# 본문이 "위 줄과 아래 줄이 만나지 않는 것이 이 그림의 뼈대"라고 직접 적는다. 그러니 두 줄을
# 나란히 두되 이어지는 세로선은 설정 하나뿐이어야 한다. 12장 대부분이 몰린 프록시가 focal.
# 타입 스펙: type-architecture.md — 브라우저부터 파드까지의 요청 경로와 관리자부터 프록시 설정까지의 제어 경로, 두 구성도가 한 지점에서 만난다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1280, 700, "KUBERNETES IN ACTION · 12장",
      "요청 하나가 지나는 길",
      "요청은 브라우저에서 파드로 흐르고, 그 길을 만드는 쪽은 관리자에서 설정으로 따로 흐른다. "
      "둘은 만나지 않고, 설정만 위로 올라가 프록시에 닿는다.",
      "12-01 과 12-02 에서 나눠 본 것들을 한 줄 위에 얹으면")

BW, GP = 220, 32
X0 = (1280 - (5 * BW + 4 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]

ddx.band(d, 100, 372, "요청 경로", x=24, w=1232)
REQ = [("브라우저", "인증서를 대조한다", None),
       ("DNS", "도메인 → 공인 IP", None),
       ("로드밸런서", "Service 소관", None),
       ("L7 프록시", "12 장 대부분이 여기", ACC),
       ("백엔드 파드", "cluster IP 를 건너뛴다", OK)]
for cx, (t, s, c) in zip(CX, REQ):
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="182" width="{BW}" height="80" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(cx - BW // 2, 182, BW, 80, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, 212, ddx.fit(t, 13, BW - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, 236, ddx.fit(s, 11, BW - 16, s), 11, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 222 L {b-BW//2-9} 222", MUTED, 1.5, m="ar")
# 세로 화살표가 CX[3] 을 지나므로 프록시 주석은 그 오른쪽에 붙인다 — 가운데 두면 관통한다
for txt, y in (("TLS 를 푼다  ·  host·경로를 가른다", 292),
               ("헤더·쿠키를 손댄다  ·  안 맞으면 default backend", 314)):
    d.t(CX[3] + 16, y, txt, 11, ACC, KR, "start")
d.t(CX[2], 292, "externalTrafficPolicy", 10, SOFT, MONO)
d.t(CX[2], 310, "Cluster 면 SNAT 로 IP 가 가려진다", 10, SOFT, KR)
d.t(CX[0], 292, "클러스터 안에 검증 주체가 없어", 10, SOFT, KR)
d.t(CX[0], 310, "인증서 불일치가 조용히 지나간다", 10, SOFT, KR)

ddx.band(d, 396, 588, "제어 경로", x=24, w=1232)
CTL = [("관리자", "kubectl apply"), ("API 서버", "오브젝트를 담는다"),
       ("Ingress 컨트롤러", "감시해 설정을 만든다"), ("프록시 설정", "nginx.conf")]
for cx, (t, s) in zip(CX, CTL):
    d.box(cx - BW // 2, 466, BW, 80, PAPER2, INFO, 1.1, 6)
    d.t(cx, 496, ddx.fit(t, 13, BW - 18, t), 13, INFO, KR, "middle", 600)
    d.t(cx, 520, ddx.fit(s, 11, BW - 16, s), 11, MUTED, KR)
for a, b in zip(CX[:4], CX[1:4]):
    d.path(f"M {a+BW//2+5} 506 L {b-BW//2-9} 506", MUTED, 1.5, m="ar")
d.path(f"M {CX[3]} 462 L {CX[3]} 266", ACC, 1.6, m="acc")
d.t(CX[3] + 14, 404, "설정만 위로 올라간다", 11, ACC, KR, "start")

d.t(24, 626, "앞의 넷이 전부 '암호가 프록시에서 풀린다'는 전제 위에 서 있어서, passthrough 를 고르면 "
             "TLS 를 푸는 일이 통째로 사라지고 호스트를 가르는 SNI 만 남는다.", 11, MUTED, KR, "start")
d.legend(650, [("제어 경로", INFO), ("12 장이 몰린 자리", ACC), ("Service 가 닿지 않는 끝", OK)])
d.save("12-full-request-journey.svg")
print("ok")
