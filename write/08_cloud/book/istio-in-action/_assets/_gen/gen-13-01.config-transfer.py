# 13-01 §7 istioctl 이 만든 설정이 VM 의 정해진 경로로 건너간다.
# 본문(원문 13.3.2 · 13.3.3): istioctl x workload entry configure 가 WorkloadGroup 의 정보와 클러스터에
#       물은 정보로 설정을 만든다. 저자는 그 내용을 넷으로 요약한다 — istiod 가 노출된 동서 게이트웨이의
#       IP 주소, istiod 인증서를 검증할 루트 인증서, WorkloadGroup 멤버로 인증할 서비스 어카운트 토큰,
#       그리고 메시와 망과 공통 속성 설정. 파일에 민감한 데이터가 들어 있으므로 안전하게 옮겨야 하며
#       시연은 SSH 위의 rsync 를 쓰지만 운영에서는 자동화돼야 하고 사람의 개입을 요구해서는 안 된다.
#       VM 안에서 옮기는 자리는 원문의 명령 그대로다 — root-cert.pem 은 /etc/certs/ 로, istio-token 은
#       파드에서와 같은 /var/run/secrets/tokens/ 로, cluster.env 는 /var/lib/istio/envoy/ 로,
#       mesh.yaml 은 /etc/istio/config/mesh 로, hosts 는 시스템 hosts 파일에 이어 붙인다.
# 타입 스펙: type-data-flow — 데이터가 칸 사이를 건너간다. 존 3 · 짐 5 · 화살표 6,
#           accent 는 민감해서 전송 방식을 정하게 만드는 짐 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 728
d = D(W, H, "ISTIO IN ACTION · 13-01 §7",
      "다섯 조각에 앉을 자리가 미리 정해져 있다",
      "WorkloadGroup 을 읽어 istioctl 이 파일 다섯을 만들고, 그것이 VM 의 정해진 경로로 간다. 색이 붙은 "
      "줄이 민감한 짐이고, 그것 때문에 전송 방식이 문제가 된다.",
      "사이드카는 자기가 파드 안인지 VM 위인지 구분하지 않습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

AX, AW = 28, 188
BX, BW = 268, 276
CX_, CW = 640, 332
TOP, RH = 148, 76

zone(AX - 8, TOP - 20, AW + 16, 5 * RH + 12, "CLUSTER")
zone(BX - 8, TOP - 20, BW + 16, 5 * RH + 12, "LOCAL SHELL")
zone(CX_ - 8, TOP - 20, CW + 16, 5 * RH + 12, "VIRTUAL MACHINE")

d.box(AX, TOP + 40, AW, 132, PAPER2, RULE, 1.0, 6)
d.t(AX + AW / 2, TOP + 70, "WorkloadGroup", 13, INK, MONO, "middle", 600)
d.t(AX + AW / 2, TOP + 92, "라벨 · 포트 · 서비스 어카운트", 11, MUTED, KR)
d.t(AX + AW / 2, TOP + 110, "망 · 준비성 프로브", 11, MUTED, KR)
d.line(AX + 16, TOP + 126, AX + AW - 16, TOP + 126, RULE, 0.9)
d.t(AX + AW / 2, TOP + 148, "istioctl 이 읽고", 11, SOFT, KR)
d.t(AX + AW / 2, TOP + 164, "나머지는 클러스터에 묻는다", 11, SOFT, KR)

rows = [
    ("root-cert.pem", "istiod 인증서를 검증한다", "/etc/certs/root-cert.pem", False),
    ("istio-token", "그룹 멤버임을 증명한다", "/var/run/secrets/tokens/istio-token", True),
    ("cluster.env", "메시와 망의 공통 설정", "/var/lib/istio/envoy/cluster.env", False),
    ("mesh.yaml", "메시 설정", "/etc/istio/config/mesh", False),
    ("hosts", "동서 게이트웨이 IP 를 담는다", "/etc/hosts 에 이어 붙인다", False),
]

for i, (name, what, dest, focal) in enumerate(rows):
    y = TOP + i * RH
    if focal:
        d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{RH - 12}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.o.append(f'<rect x="{CX_}" y="{y}" width="{CW}" height="{RH - 12}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(BX, y, BW, RH - 12, PAPER2, RULE, 1.0, 6)
        d.box(CX_, y, CW, RH - 12, PAPER2, RULE, 1.0, 6)
    d.t(BX + 16, y + 26, name, 12, ACC if focal else INK, MONO, "start", 600)
    d.t(BX + 16, y + 46, what, 11, MUTED, KR, "start")
    d.t(CX_ + 16, y + 26, dest, 11, ACC if focal else INK, MONO, "start")
    d.t(CX_ + 16, y + 46, "istio-agent 가 여기서 읽는다" if i == 0 else
        ("파드에서와 같은 디렉토리" if focal else ""), 11, MUTED, KR, "start")
    d.arrow([(BX + BW, y + (RH - 12) / 2), (CX_ - 2, y + (RH - 12) / 2)],
            ACC if focal else MUTED, "acc" if focal else "ar", 1.5 if focal else 1.2)

d.path(f"M {AX + AW} {TOP + 106} L {BX - 2} {TOP + 106}", INFO, 1.3, m="info")
d.chip((AX + AW + BX) / 2, TOP + 84, "생성", INFO, 9)
d.chip((BX + BW + CX_) / 2, TOP - 2, "rsync · SSH", MUTED, 9)

d.t(28, 588, "저자가 요약한 네 가지 내용 — 동서 게이트웨이 IP · 루트 인증서 · 서비스 어카운트 토큰 · 메시와 망 설정", 11, SOFT, KR, "start")
d.t(28, 612, "토큰이 들어 있어 전송이 문제가 된다 — 시연은 SSH 위의 rsync 이고 운영에서는 사람의 개입이 없어야 한다", 11, MUTED, KR, "start")
d.t(28, 636, "hosts 가 필요한 이유 — 아직 컨트롤 플레인에 붙지 않아 DNS 프록시에 항목이 하나도 없다", 11, SOFT, KR, "start")
d.t(28, 660, "옮긴 뒤에는 소유권을 istio-proxy 에 주고 systemctl 로 에이전트를 시작한다", 11, MUTED, KR, "start")
d.legend(680, [("민감해서 전송 방식을 정하게 만드는 짐", ACC), ("설정을 만드는 근거", INFO)])
d.save("13-01.config-transfer.svg")
