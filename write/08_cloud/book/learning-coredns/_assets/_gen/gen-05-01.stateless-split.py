# 05-01 §4 — 영속 상태는 etcd 클러스터에 모으고 CoreDNS 는 무상태로 늘린다.
# 원문 근거: "all of the persistent state (data) is stored in etcd. CoreDNS connects to etcd and reads
#            data as needed" / "Running as a stateless service also makes it much simpler to scale
#            CoreDNS; we can run many instances behind a load balancer" / "as long as more than half of
#            the instances are up ... etcd will keep running" / 세 인스턴스면 하나를 잃어도 동작한다.
# 버전 칩의 근거: 원서 Example 5-8 의 기동 로그가 CoreDNS-1.3.1, Example 5-2 가 etcd 3.3.11.
# 타입 스펙: type-deployment — 존 경계·복제 수·배포 산출물이 논지이고, 상태가 어느 존에 있는지가 결론이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W, H = 880, 664
d = D(W, H, "LEARNING COREDNS · 05-01 §4",
      "상태는 아래에 모으고 위는 몇 대든 늘린다",
      "윗단의 CoreDNS 는 자기 상태를 갖지 않아 어느 인스턴스가 답해도 결과가 같다. "
      "영속 상태는 전부 아랫단의 etcd 에 있고, 쿼럼만 살아 있으면 하나를 잃어도 계속 돈다.",
      "주황 테두리가 잃으면 안 되는 자리입니다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{PAPER}" '
               f'stroke="{RULE}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    d.o.append(f'<rect x="{x + 14}" y="{y - 8}" width="{len(label) * 9 + 20}" height="16" fill="{PAPER}"/>')
    d.t(x + 22, y + 4, label, 9, SOFT, MONO, "start", 600)


def tag(x, y, txt):
    d.o.append(f'<rect x="{x}" y="{y}" width="{len(txt) * 7 + 14}" height="16" rx="2" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + 7, y + 12, txt, 9, SOFT, MONO, "start", 600)


def badge(xr, y, txt, c=MUTED):
    w = len(txt) * 7 + 14
    d.o.append(f'<rect x="{xr - w}" y="{y}" width="{w}" height="16" rx="2" '
               f'fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
    d.t(xr - w / 2, y + 12, txt, 9, c, MONO)


def chip(x, y, w, name, ver):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="4" fill="{PAPER2}" stroke="{MUTED}" stroke-width="0.8"/>')
    d.t(x + 10, y + 17, name, 12, INK, MONO, "start")
    d.t(x + w - 10, y + 17, ver, 9, MUTED, MONO, "end")


zone(184, 116, 656, 200, "STATELESS · QUERY")
zone(184, 380, 656, 152, "STATEFUL · QUORUM")

d.box(20, 160, 136, 76, PAPER2, RULE, 1.0)
d.t(88, 192, "클라이언트", 14, INK, KR, "middle", 600)
d.t(88, 216, "resolver", 11, MUTED, MONO)

d.box(212, 156, 232, 84, PAPER2, RULE, 1.0)
tag(224, 148, "LB")
d.t(328, 200, "로드 밸런서", 15, INK, KR, "middle", 600)
d.t(328, 224, "앞단 하나", 12, MUTED, KR)

d.box(512, 148, 300, 140, PAPER2, RULE, 1.0)
tag(524, 140, "PROCESS")
badge(800, 140, "x3")
d.t(662, 186, "CoreDNS 인스턴스", 15, INK, KR, "middle", 600)
d.t(662, 210, "고유한 상태가 없다", 12, MUTED, KR)
chip(536, 240, 252, "coredns", "v1.3.1")

d.tone(212, 412, 600, 96, ACC, 6, "0E", 1.4)
tag(224, 404, "CLUSTER")
badge(800, 404, "x3", ACC)
d.t(512, 448, "etcd 클러스터", 15, ACC, KR, "middle", 600)
chip(360, 468, 304, "etcd", "v3.3.11")

d.arrow([(158, 198), (208, 198)], INFO, "info", 1.4)
d.t(183, 186, "DNS · 53", 9, INFO, MONO)
d.arrow([(446, 198), (508, 198)], MUTED, "ar", 1.4)
d.t(477, 186, "질의", 12, MUTED, KR)
d.path("M 662 292 L 662 408", ACC, 1.4, m="acc")
d.t(676, 344, "etcdv3 · 2379", 12, ACC, MONO, "start")

d.t(20, 560, "쿼럼은 절반 초과다 — 셋 중 하나를 잃어도 읽기와 쓰기가 계속된다", 13, MUTED, KR, "start")
d.t(20, 584, "윗단의 인스턴스는 죽어도 잃을 정보가 없어서 그냥 다시 띄우면 된다", 13, MUTED, KR, "start")

d.legend(620, [("상태를 쥔 자리와 그 경로", ACC), ("클라이언트가 들어오는 경로", INFO)])
d.save("05-01.stateless-split.svg")
