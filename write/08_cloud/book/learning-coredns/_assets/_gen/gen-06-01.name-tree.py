# 06-01 §5 — 클러스터 도메인 아래에서 이름이 갈리는 자리.
# 본문 근거: 이 노트 §5 「명세가 이름을 미리 못 박아 둔다」.
# 원서 쪽: p.6-7 "The DNS Specification for Kubernetes... All records in the specification fall under a
#          single domain, the cluster domain... cluster.local" /
#          p.6-7 Service Records: service.namespace.svc.cluster-domain, Example 6-3(p.7) /
#          p.15 Pod Records (deprecated): a-b-c-d.namespace.pod.cluster.local.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계보이고 갈래마다 결과가 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 940, 656
d = D(W, H, "LEARNING COREDNS · 06-01 §5",
      "클러스터 도메인 아래 이름이 갈리는 자리",
      "명세의 모든 레코드는 클러스터 도메인 하나 아래 들어간다. 그 아래에서 svc 갈래와 pod 갈래가 "
      "나뉘고, 왼쪽 갈래만 Service 선언에서 유도되며 오른쪽 갈래는 현행 명세 1.1.0 에서 빠졌다.",
      "붉은 갈래는 명세가 스스로 걷어낸 자리입니다")

NW, NH = 260, 56
ROOT_Y, L2_Y, L3_Y, L4_Y = 100, 208, 316, 424
LX, RX = 250, 690

d.line(470, ROOT_Y + NH, 470, 176, MUTED, 1.0)
d.line(LX, 176, RX, 176, MUTED, 1.0)
for cx in (LX, RX):
    d.line(cx, 176, cx, L2_Y, MUTED, 1.0)
    d.line(cx, L2_Y + NH, cx, L3_Y, MUTED, 1.0)
    d.line(cx, L3_Y + NH, cx, L4_Y, MUTED, 1.0)


def node(cx, y, name, sub, c=INK, tone=False):
    if tone:
        d.tone(cx - NW / 2, y, NW, NH, c, 6, "12", 1.4)
    else:
        d.box(cx - NW / 2, y, NW, NH, PAPER2, RULE, 1.0)
    d.t(cx, y + 26, name, 14, c, MONO, "middle", 600)
    if sub:
        d.t(cx, y + 46, sub, 13, MUTED, KR)


node(470, ROOT_Y, "cluster.local", "클러스터 도메인 · 설정 변경 가능")
node(LX, L2_Y, "svc", "Service 선언 기반 유도", OK, True)
node(RX, L2_Y, "pod", "현행 명세 제외 갈래", BAD, True)
node(LX, L3_Y, "<namespace>", "")
node(RX, L3_Y, "<namespace>", "")
node(LX, L4_Y, "<service>", "레코드 생성 지점")
node(RX, L4_Y, "a-b-c-d", "파드 존재 확인 없음")

d.t(LX, 512, "A/AAAA · SRV", 15, ACC, MONO, "middle", 600)
d.t(LX, 534, "clusterIP: 단일 주소 / None: Ready 엔드포인트 수만큼", 13, MUTED, KR)
d.t(LX, 556, "_포트이름._프로토콜 접두 시 SRV 생성", 13, MUTED, KR)
d.t(RX, 512, "A 레코드 한정", 15, BAD, KR, "middle", 600)
d.t(RX, 534, "와일드카드 인증서 용도", 13, MUTED, KR)
d.t(RX, 556, "DNS 신원 보장 약화", 13, MUTED, KR)

d.legend(584, [("선언 기반 유도 갈래", OK), ("현행 명세 제외 갈래", BAD), ("최종 생성 레코드", ACC)])
d.save("06-01.name-tree.svg")
