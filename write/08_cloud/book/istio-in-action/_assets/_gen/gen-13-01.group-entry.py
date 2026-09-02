# 13-01 §3 WorkloadGroup · WorkloadEntry · 쿠버네티스 서비스의 관계 — 원문 그림 13.5.
# 본문(원문 13.1.2): WorkloadGroup 은 Deployment 와 비슷하게 자기가 관리하는 워크로드가 어떻게 구성되는지의
#       템플릿을 정의한다 — 노출 포트, 인스턴스에 붙일 라벨, 메시에서 신원이 될 서비스 어카운트,
#       애플리케이션 건강 검사 방법. WorkloadEntry 는 Pod 와 비슷하게 사용자 트래픽을 처리하는 VM 하나를
#       나타내고, 공통 속성에 더해 인스턴스의 주소와 헬스 상태라는 고유 속성을 갖는다. 그것이 중요한 이유는
#       쿠버네티스 서비스나 ServiceEntry 가 라벨 셀렉터로 그것을 골라 트래픽의 백엔드로 쓸 수 있기 때문이다.
# 필드 이름은 원문 13.3.2 의 WorkloadGroup YAML 과 13.3.5 의 WorkloadEntry 출력에서 그대로 가져왔다.
# 타입 스펙: type-er — 엔티티와 카디널리티가 이야기다. 상속도 연산도 없으므로 uml-class 가 아니다.
#           엔티티는 헤더(타입 태그 + 이름) + 필드 목록, 관계선에 양 끝 카디널리티, coral 은 중심 엔티티에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 640
d = D(W, H, "ISTIO IN ACTION · 13-01 §3",
      "템플릿 하나가 인스턴스 여럿을 찍고 서비스가 그것을 고른다",
      "WorkloadGroup 이 공통 속성을 정의하고 WorkloadEntry 가 VM 하나를 나타낸다. 색이 붙은 엔티티가 "
      "이 그림의 중심이며, 주소를 가진 유일한 자리이자 서비스가 라벨로 고르는 대상이다.",
      "Deployment 와 Pod 의 관계를 그대로 옮겨 온 구조입니다")

def entity(x, y, w, tag, name, fields, focal=False):
    hh, fh = 46, 22
    h = hh + fh * len(fields) + 12
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.line(x, y + hh, x + w, y + hh, RULE, 0.9)
    d.t(x + 16, y + 20, tag, 8, SOFT, MONO, "start", 600)
    d.t(x + 16, y + 38, name, 13, ACC if focal else INK, MONO, "start", 600)
    for i, f in enumerate(fields):
        d.t(x + 16, y + hh + 16 + i * fh, f, 9.5, MUTED, MONO, "start")
    return h

AX, BX, CX = 36, 468, 908
AW, BW, CW = 336, 344, 288
AY, BY, CY = 132, 132, 168

ah = entity(AX, AY, AW, "ENTITY · 템플릿", "WorkloadGroup", [
    "# metadata.name        forum",
    "metadata.labels        app: forum",
    "template.ports         http: 8080",
    "template.serviceAccount  forum-sa",
    "template.network       vm-network",
    "probe                  httpGet /api/healthz",
])
bh = entity(BX, BY, BW, "ENTITY · 인스턴스", "WorkloadEntry", [
    "# metadata.name        forum-<주소>-<망>",
    "spec.address           VM 의 주소",
    "spec.labels            그룹에서 물려받는다",
    "spec.network           vm-network",
    "spec.serviceAccount    forum-sa",
    "status.conditions      Healthy: True | False",
], focal=True)
ch = entity(CX, CY, CW, "ENTITY · 고르는 쪽", "Service", [
    "# metadata.name        forum",
    "spec.ports             80 -> 8080",
    "spec.selector          app: forum",
])

my = AY + ah / 2
d.path(f"M {AX + AW} {my} H {BX - 2}", MUTED, 1.2, m="ar")
d.chip((AX + AW + BX) / 2, my - 22, "템플릿이 된다", MUTED, 9)
d.t(AX + AW + 16, my + 16, "1", 8, SOFT, MONO, "start", 600)
d.t(BX - 16, my + 16, "N", 8, SOFT, MONO, "end", 600)

cy_mid = CY + ch / 2
d.path(f"M {CX} {cy_mid} H {BX + BW + 2}", MUTED, 1.2, m="ar")
d.chip((BX + BW + CX) / 2, cy_mid - 22, "라벨로 고른다", MUTED, 9)
d.t(CX - 16, cy_mid + 16, "1", 8, SOFT, MONO, "end", 600)
d.t(BX + BW + 16, cy_mid + 16, "N", 8, SOFT, MONO, "start", 600)

FY = 396
d.box(36, FY, 1168, 92, PAPER2, RULE, 1.0, 6)
d.t(56, FY + 26, "쿠버네티스에서 그대로 옮겨 온 대응", 11, ACC, KR, "start", 600)
d.t(56, FY + 50, "Deployment  ->  WorkloadGroup            복제본을 어떻게 만들지의 설정을 담는다", 11, INK, MONO, "start")
d.t(56, FY + 72, "Pod         ->  WorkloadEntry            고유한 것이 없어서 버리고 갈아 끼울 수 있다", 11, INK, MONO, "start")

d.t(36, 524, "자동 등록 — 워크로드가 토큰으로 그룹 멤버임을 인증하면 컨트롤 플레인이 WorkloadEntry 를 만든다", 11, SOFT, KR, "start")
d.t(36, 548, "자동 정리 — VM 을 지우면 그 WorkloadEntry 도 사라진다. 만들어지는 것만큼 치워지는 것도 중요하다", 11, MUTED, KR, "start")
d.legend(568, [("주소를 가진 유일한 자리", ACC), ("템플릿과 고르는 쪽", MUTED)])
d.save("13-01.group-entry.svg")
