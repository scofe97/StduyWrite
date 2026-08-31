# 01-01 §7 마이크로서비스가 아니어도 붙는다.
# 본문: 프록시가 애플리케이션 밖에 살기 때문에 기존 시스템을 바꾸지 않고 편입시킬 수 있다.
#       모놀리스라면 인스턴스마다 서비스 프록시를 함께 배포해 트래픽을 투명하게 처리하게 한다.
#       최소한 요청 메트릭을 얻고, 어느 서비스가 이것과 통신해도 되는지 정책 강제에도 참여시킬 수 있다.
# 타입 스펙: type-deployment — 무엇이 어디에 놓이는지가 논점이다. 존 3 · 노드 4 · 경로 2,
#           accent 는 원서가 겨냥하지 않았는데도 편입되는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1200, 600
d = D(W, H, "ISTIO IN ACTION · 01-01 §7",
      "프록시가 밖에 살아서 기존 시스템도 들어온다",
      "저자는 Istio 가 마이크로서비스를 겨냥하지만 거기 한정되지 않는다고 명시한다. 근거는 프록시가 "
      "애플리케이션 밖에 산다는 것 하나다. 색이 붙은 자리가 코드를 바꾸지 않고 편입되는 쪽이다.",
      "라이브러리로 이미 레질리언스를 구현한 옛 서비스도 같은 방식으로 들어옵니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="40" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 32, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 62, y + 24, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 62, y + 42, sub, 9, MUTED, MONO, "start")

zone(56, 148, 500, 100, "KUBERNETES")
zone(56, 292, 500, 100, "VIRTUAL MACHINE")
zone(640, 148, 504, 244, "SAME MESH")

node(80, 176, 452, 60, "POD", "새 마이크로서비스", "app + istio-proxy")
node(80, 320, 452, 60, "VM", "모놀리스", "app + istio-proxy", focal=True)
node(664, 176, 456, 60, "CP", "컨트롤 플레인", "설정 · 아이덴티티 · 텔레메트리")
node(664, 320, 456, 60, "OPS", "얻는 것", "요청 메트릭 · 정책 강제")

d.path("M 532 206 L 620 206 L 620 206 L 660 206", INFO, 1.2, m="info")
d.path("M 532 350 L 620 350 L 620 350 L 660 350", ACC, 1.5, m="acc")
d.t(600, 188, "같은 방식", 9, MUTED, KR, "middle")
d.t(600, 332, "코드 변경 없이", 9, ACC, KR, "middle", 600)

d.t(32, 448, "모놀리스에서 최소한 얻는 것 — 사용량 · 지연 · 처리량 · 실패 특성", 11, SOFT, KR, "start")
d.t(32, 472, "저자가 든 정책 예 — \"클라우드 서비스는 온프레미스 애플리케이션과 통신하거나 그 데이터를 쓸 수 없다\"", 11, MUTED, KR, "start")
d.t(32, 496, "옛 서비스에 서킷 브레이커가 남아 있어도 더 제한적인 쪽이 이긴다 — 다만 타임아웃과 재시도는 충돌할 수 있다", 11, SOFT, KR, "start")
d.legend(536, [("코드를 바꾸지 않고 편입되는 자리", ACC), ("메시가 원래 겨냥한 쪽", INFO)])
d.save("01-01.brownfield.svg")
