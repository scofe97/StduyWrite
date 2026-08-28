# 06-01.traffic-gateways — 나가는 길과 들어오는 길이 다르다
# 본문 요구: "NAT 는 나가기만, IGW 는 양방향, ELB 4종은 계층이 다르다" + ELB 넷의 성격.
# 타입 스펙: type-layers.md — 통제·부품을 묶음으로 세우는 control catalog 패턴이 이 타입으로 간다.
#           2026-08-28 렌더 확인 후 재분류: 앞서 행 대조로 적었으나 윗줄 2칸과 아랫줄 4칸의
#           열이 서로 대응하지 않아 격자가 아니다. 방향 관문 층과 ELB 계층 층, 두 띠다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 528
d = D(W, H, "AWS · WAYS IN AND OUT",
      "나가는 길과 들어오는 길을 따로 본다",
      "NAT 는 나가기만, IGW 는 양방향, ELB 넷은 서로 다른 계층에서 들어오는 트래픽을 받는다.",
      lead="관문마다 방향과 계층이 달라 장애 때 볼 곳이 갈린다")

TY, TH = 152, 96
for x, w, nm, sub, arrow, c in ((32, 452, "NAT 디바이스", "사설 인스턴스가 인터넷으로 나갈 때", "밖으로만", INFO),
                                (516, 452, "IGW", "VPC 에 부착 + 라우팅 + NACL·SG 허용", "양방향", INFO)):
    d.box(x, TY, w, TH, PAPER2, c, 1.1, 6)
    d.t(x + w // 2, TY + 34, nm, 14, c, KR, "middle", 600)
    d.t(x + w // 2, TY + 60, ddx.fit(sub, 12, w - 24, sub), 12, MUTED, KR)
    d.t(x + w // 2, TY + 82, arrow, 11, SOFT, KR)

EY, EH, EW = TY + TH + 40, 128, 224
ELB = [("Classic", "EC2 기본 밸런싱", "컨테이너와 쓰지 말 것", WARN),
       ("ALB", "L7 — 헤더·경로 라우팅", "EKS 에서 쓰는 쪽", ACC),
       ("NLB", "L4 — TCP/UDP 포트", "EIP 를 붙일 수 있는 유일한 LB", INFO),
       ("Gateway", "VPC 수준 어플라이언스", "EKS 생태계에서는 미사용", WARN)]
d.t(36, EY - 14, "ELB 넷 — 같은 자리 같아 보이지만 계층이 다르다", 12, SOFT, KR, "start")
for i, (nm, layer, note, c) in enumerate(ELB):
    x = 32 + i * (EW + 12)
    if c is ACC:
        d.tone(x, EY, EW, EH, ACC, 6, "12", 1.4)
    else:
        d.box(x, EY, EW, EH, PAPER2, c, 1.1, 6)
    d.t(x + EW // 2, EY + 34, nm, 13, c, MONO, "middle", 600)
    d.t(x + EW // 2, EY + 62, ddx.fit(layer, 11, EW - 20, layer), 11, MUTED, KR)
    d.t(x + EW // 2, EY + 90, ddx.fit(note, 11, EW - 20, note), 11, SOFT, KR)

d.t(36, EY + EH + 40, "IGW 를 붙였는데도 안 되면 라우팅 테이블과 NACL·SG 순서로 보고, 나가는 길만 막혔으면 NAT 를 본다",
    12, MUTED, KR, "start")
d.legend(EY + EH + 52, [("경로 부품", INFO), ("피하거나 안 쓰는 것", WARN), ("EKS 가 쓰는 것", ACC)])
d.save("06-01.traffic-gateways.svg")
print("ok traffic-gateways")
