# 13-01 §5 클러스터 호스트명이 VM 에서 풀리는 흐름 — 원문 그림 13.14.
# 본문(원문 13.4.1) 다섯 단계: (1) 클라이언트가 webapp.istioinaction 을 묻는다. (2) 운영체제가 처리하며
#       hosts 파일에 맞는 항목이 있는지 먼저 본다. 없으면 기본 리졸버로 넘긴다. (3) Ubuntu 의 기본 리졸버는
#       systemd-resolved 이고 루프백 127.0.0.53 의 53 번을 듣는데, istio-agent 가 건 Iptable 규칙 때문에
#       요청이 거기 닿지 못하고 DNS 프록시로 돌려진다. (4) DNS 프록시는 메시가 아는 서비스의 항목을 갖고
#       있어서 이름이 맞으면 해석한다 — webapp.istioinaction 은 NDS 로 설정돼 있으므로 여기서 풀린다.
#       (5) 클러스터 서비스가 아니면 resolv.conf 의 네임서버로 폴백해 거기서 풀리거나 실패한다.
#       포트 15053 과 규칙 두 줄은 원문의 iptables-save · netstat 출력에서 가져왔다.
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, 출구 2) · 사각형(행동).
#           예는 오른쪽, 아니오는 아래, 모든 갈래에 라벨, accent 는 갈래 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 936
d = D(W, H, "ISTIO IN ACTION · 13-01 §5",
      "가로채기가 없으면 이름은 기계 밖으로 나간다",
      "질의는 평소의 리졸버로 가려다가 Iptable 규칙에 붙들려 사이드카 안의 DNS 프록시로 향한다. "
      "색이 붙은 자리가 그 가로채기이고, 그것이 없으면 클러스터 이름은 어디서도 풀리지 않는다.",
      "이름이 풀리지 않으면 요청은 애플리케이션을 떠나지도 못합니다")

def oval(x, y, w, h, label, sub=None):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 22)
    d.t(x + w / 2, y + (h / 2 + 5 if not sub else 24), label, 13, INK, KR, "middle", 600)
    if sub: d.t(x + w / 2, y + 44, sub, 11, MUTED, MONO)

def step(x, y, w, h, label, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, label, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 9, MUTED, MONO)

def diamond(cx, cy, l1, l2):
    d.o.append(f'<path d="M {cx-172} {cy} L {cx} {cy-56} L {cx+172} {cy} L {cx} {cy+56} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy - 4, l1, 12, INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, INK, KR, "middle", 600)

CA, CB = 236, 752

oval(CA - 168, 112, 336, 64, "webapp.istioinaction 을 묻는다", "01 · 애플리케이션의 DNS 질의")
diamond(CA, 268, "hosts 파일에", "맞는 항목이 있나")
oval(CB - 150, 240, 300, 56, "그 값으로 끝난다")
step(CA - 168, 384, 336, 68, "기본 리졸버로 간다", "02 · systemd-resolved 127.0.0.53:53")
step(CA - 168, 508, 336, 68, "Iptable 규칙이 붙든다", "03 · REDIRECT --to-ports 15053", focal=True)
diamond(CA, 664, "DNS 프록시가", "아는 이름인가")
oval(CB - 190, 636, 380, 56, "주소를 돌려준다")
oval(CA - 180, 796, 360, 56, "resolv.conf 네임서버로 폴백")

d.arrow([(CA, 176), (CA, 214)], MUTED, "ar", 1.4)
d.arrow([(CA, 324), (CA, 380)], MUTED, "ar", 1.4)
d.arrow([(CA, 452), (CA, 504)], ACC, "acc", 1.5)
d.arrow([(CA, 576), (CA, 610)], MUTED, "ar", 1.4)
d.arrow([(CA, 720), (CA, 794)], MUTED, "ar", 1.4)
d.arrow([(CA + 172, 268), (CB - 152, 268)], MUTED, "ar", 1.4)
d.arrow([(CA + 172, 664), (CB - 192, 664)], MUTED, "ar", 1.4)

d.t((CA + CB) / 2, 256, "예", 12, MUTED, KR, "middle", 600)
d.t((CA + CB) / 2, 652, "예", 12, MUTED, KR, "middle", 600)
d.t(CA + 20, 352, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 20, 752, "아니오", 12, MUTED, KR, "start", 600)

d.t(CB - 190, 736, "여기서 풀리는 이유 — istiod 가 NDS 로", 11, SOFT, KR, "start")
d.t(CB - 190, 758, "메시가 아는 서비스를 채워 두기 때문", 11, SOFT, KR, "start")
d.t(CB - 190, 786, "짧은 변형은 agent 가 만든다", 11, MUTED, KR, "start")
d.t(CB - 190, 808, "webapp.istioinaction.svc 등", 11, MUTED, MONO, "start")

d.t(24, 876, "가로채기가 UDP 와 TCP 양쪽에 걸린다 — 규칙 두 줄이 127.0.0.53 의 53 번을 15053 으로 돌린다", 11, SOFT, KR, "start")
d.legend(894, [("가로채기 — 이 한 걸음이 전부를 가른다", ACC), ("평소의 해석 경로", MUTED)])
d.save("13-01.dns-resolution.svg")
