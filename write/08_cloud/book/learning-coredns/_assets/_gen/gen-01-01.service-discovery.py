# 01-01 §1 — 컨테이너가 동적으로 뜨고 지는 환경에서 상대를 찾는 경로.
# 원문 근거: 데이터베이스 서비스 컨테이너가 인가 서비스를 호출해야 하는데
#            인가 컨테이너가 부하에 따라 기동·정지되어 "실행 중인 목록"을 얻어야 한다.
#            답은 DNS 이고, CoreDNS 의 최대 강점은 etcd·Kubernetes 같은 오케스트레이터와 통신하는 능력이다.
# 타입 스펙: type-architecture — 구성요소와 연결이 논지이고 오른쪽 존이 수명 경계다.
# 캔버스는 880 폭 — viewBox 가 좁을수록 본문에서 글자가 크게 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W, H = 880, 540
d = D(W, H, "LEARNING COREDNS · 01-01 §1",
      "이름 하나로 흔들리는 집합을 가리킨다",
      "데이터베이스 서비스 컨테이너가 인가 서비스를 호출하려면 지금 떠 있는 인가 컨테이너의 IP 를 알아야 한다. "
      "그 목록은 부하에 따라 바뀌므로 호출자가 들고 있을 수 없고, DNS 가 이름을 현재 IP 집합으로 바꿔 준다.",
      "오른쪽 존의 구성원은 부하에 따라 늘고 줄어듭니다")

ZX, ZY, ZW, ZH = 660, 100, 200, 248
d.box(ZX, ZY, ZW, ZH, PAPER, RULE, 0.8, 8)
d.o.append(f'<rect x="{ZX + 10}" y="{ZY + 3}" width="176" height="16" rx="2" fill="{PAPER}"/>')
d.t(ZX + 14, ZY + 15, "인가 서비스 · 부하 따라 증감", 10, SOFT, KR, "start")

d.arrow([(220, 220), (348, 220)], MUTED, "ar", 1.4)
d.t(290, 208, "이름으로 질의", 13, MUTED, KR)
d.arrow([(360, 254), (232, 254)], MUTED, "ar", 1.4)
d.t(296, 274, "현재 IP 집합", 13, MUTED, KR)
d.path("M 460 148 L 460 192", MUTED, 1.2, m="ar", dash="4 3")
d.t(472, 176, "떠 있는 집합", 13, MUTED, KR, "start")
d.path("M 120 276 L 120 396 L 760 396 L 760 352", INFO, 1.4, m="ar")
d.t(440, 416, "얻은 IP 로 직접 통신", 13, INFO, KR)

d.box(20, 200, 200, 76, PAPER2, RULE, 1.0, 8)
d.t(120, 232, "데이터베이스 서비스", 14, INK, KR, "middle", 600)
d.t(120, 254, "호출하는 쪽", 12, MUTED)

d.box(360, 92, 200, 56, PAPER2, RULE, 1.0, 8)
d.t(460, 118, "오케스트레이터", 14, INK, KR, "middle", 600)
d.t(460, 138, "etcd · Kubernetes", 12, MUTED, MONO)

d.tone(360, 192, 200, 84, ACC, 8, "12", 1.4)
d.t(460, 224, "CoreDNS", 16, ACC, MONO, "middle", 600)
d.t(460, 250, "이름을 IP 집합으로", 13, MUTED)

for i, (nm, sub) in enumerate([("인가 컨테이너 1", "실행 중"),
                               ("인가 컨테이너 2", "실행 중"),
                               ("인가 컨테이너 3", "방금 기동")]):
    y = 132 + i * 72
    d.tone(672, y, 176, 56, INFO, 6, "14", 1.2)
    d.t(760, y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(760, y + 43, sub, 12, INFO, KR)

d.legend(452, [("이름을 IP 집합으로 바꾸는 자리", ACC), ("수명이 짧은 구성원", INFO)])
d.save("01-01.service-discovery.svg")
