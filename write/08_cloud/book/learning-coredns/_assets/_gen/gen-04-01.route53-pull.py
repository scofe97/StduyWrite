# 04-01 §6 — route53 플러그인이 Route 53 의 존 데이터를 API 로 당겨 와 메모리 사본으로 답하는 흐름.
# 근거(CoreDNS v1.15.0, 2026-11-02 대조):
#   plugin/route53/route53.go Run — 시작할 때 updateZones 를 한 번 돌리고, 이후 h.refresh 마다 다시 돈다.
#   plugin/route53/route53.go updateZones — Hosted Zone ID 마다 ListResourceRecordSets 를 부르고,
#       받은 레코드로 file.NewZone 을 새로 만들어 (*z[i]).z = newZ 로 통째로 바꿔 끼운다.
#   plugin/route53/setup.go:68 — refresh 기본값 time.Duration(1) * time.Minute.
#   plugin/route53/README.md — 자격증명은 환경 변수, 공유 자격증명 파일, EC2 인스턴스 역할 순으로 찾는다.
# 타입 스펙: type-flowchart — 원본에서 사본을 거쳐 클라이언트로 가는 한 방향 흐름이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR

W, H = 880, 368
d = D(W, H, "LEARNING COREDNS · 04-01 §6",
      "Route 53 원본을 API 로 당겨 사본으로 답한다",
      "원본은 Route 53 에 있고, CoreDNS 는 시작할 때 한 번 그리고 refresh 마다 AWS API 로 레코드를 받아 메모리 사본을 만든다. "
      "클라이언트의 질의는 그 사본이 답한다.",
      "주황 상자가 클라이언트에 답하는 사본입니다")

BY, BH = 124, 92
BW = 184
X1, X2, X3 = 20, 348, 676


def node(x, name, sub, focal=False):
    if focal:
        d.tone(x, BY, BW, BH, ACC, 6, "12", 1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, BY + 40, name, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + BW / 2, BY + 64, sub, 12, MUTED)


node(X1, "Route 53", "원본 · Hosted Zone")
node(X2, "CoreDNS", "route53 의 메모리 사본", focal=True)
node(X3, "클라이언트", "CoreDNS 에 묻는 쪽")

# 원본 → 사본: 당겨 오는 흐름
d.arrow([(X1 + BW + 4, 168), (X2 - 4, 168)], MUTED, "ar", 1.4)
d.t((X1 + BW + X2) / 2, 148, "AWS API 호출", 12, MUTED, KR)
d.t((X1 + BW + X2) / 2, 192, "시작 시 + refresh 1m", 12, MUTED, KR)

# 사본 → 클라이언트: 답, 반대로 질의
d.arrow([(X2 + BW + 4, 152), (X3 - 4, 152)], ACC, "acc", 1.6)
d.t((X2 + BW + X3) / 2, 136, "사본으로 응답", 12, ACC, KR)
d.arrow([(X3 - 4, 188), (X2 + BW + 4, 188)], MUTED, "ar", 1.2, "5 4")
d.t((X2 + BW + X3) / 2, 212, "질의", 12, MUTED, KR)

d.t(20, 256, "필요한 것 · Hosted Zone ID · AWS 자격증명", 13, MUTED, KR, "start")
d.t(20, 280, "존 전송이 아니라 ListResourceRecordSets API 호출", 13, MUTED, KR, "start")
d.t(20, 304, "갱신마다 사본을 통째로 교체", 13, MUTED, KR, "start")

d.legend(320, [("클라이언트에 답하는 사본", ACC)])
d.save("04-01.route53-pull.svg")
