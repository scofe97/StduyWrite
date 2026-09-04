# a0-04 §1 사이드카의 포트가 향하는 두 방향.
# 본문(부록 D.1): 서비스용 다섯(15020 · 15021 · 15053 · 15001 · 15006)과 디버깅용 넷
#       (15000 · 15090 · 15004 · 15020). 15020 이 두 축에 걸친다. 15021 의 헬스 체크는
#       Envoy 가 15020 의 파일럿 에이전트로 넘겨 거기서 실제 판정이 일어난다.
# 타입 스펙: type-deployment — 무엇이 어느 경계 안에 서고 어느 방향을 향하는지가 논점이다.
#           존 2 · 포트 노드 · 경로, accent 는 두 축에 걸친 포트 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · A0-04 §1",
      "여덟이 두 방향으로 갈린다",
      "왼쪽은 다른 서비스를 향해 열린 다섯이고 오른쪽은 사람이 들여다보려고 열린 넷이다. "
      "색이 붙은 15020 만 두 축에 걸쳐 있어 양쪽에 다 나온다.",
      "15001 과 15006 은 istio-init 이 세운 Iptable 규칙과 짝입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    # 존 라벨이 한글이라 8px eyebrow 관례를 쓸 수 없다(계약 하한 11px). 마스크도 함께 키운다.
    tw = int(sum(11 if '가' <= c <= '힣' else 6.9 for c in label)) + 20
    d.o.append(f'<rect x="{x + 12}" y="{y - 9}" width="{tw}" height="18" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 11, SOFT, KR, "start", 600)

PW, PH = 400, 52
def port(x, y, num, what, focal=False, c=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 32, num, 14, ACC if focal else (c or INK), MONO, "start", 600)
    d.t(x + 92, y + 32, what, 11, MUTED, KR, "start")

zone(28, 148, 440, 356, "서비스를 향한 다섯")
zone(532, 148, 440, 296, "사람을 향한 넷")

LY = [176, 244, 312, 380, 440]
port(48, LY[0], "15020", "메트릭 · 헬스 체크", focal=True)
port(48, LY[1], "15021", "준비 상태를 확인받는다")
port(48, LY[2], "15053", "로컬 DNS 프록시")
port(48, LY[3], "15001", "아웃바운드가 돌려진다", c=INFO)
port(48, LY[4], "15006", "인바운드가 돌려진다", c=INFO)

RY = [176, 244, 312, 380]
port(552, RY[0], "15000", "Envoy 관리 인터페이스")
port(552, RY[1], "15090", "Envoy 프록시 메트릭")
port(552, RY[2], "15004", "Pilot 디버그를 대신 연다")
port(552, RY[3], "15020", "에이전트 디버그", focal=True)

d.path("M 448 202 L 490 202 L 490 406 L 548 406", ACC, 1.5, m="acc", dash="5 4")
d.t(494, 300, "같은 포트", 11, ACC, KR, "start", 600)
d.t(494, 322, "두 축에", 11, ACC, KR, "start", 600)
# 헬스 체크는 15021 이 받아 15020 으로 넘긴다. 화살표는 아래에서 위로 간다.
d.arrow([(200, 242), (200, 230)], MUTED, "ar", 1.3)
d.t(216, 236, "판정은 위에서", 11, SOFT, KR, "start")

d.t(28, 540, "15021 은 확인받는 자리이고 실제 판정은 15020 의 파일럿 에이전트가 한다 — 두 포트가 한 일을 나눠 갖는다", 11, SOFT, KR, "start")
d.legend(560, [("두 축에 걸친 포트", ACC), ("Iptable 규칙과 짝인 포트", INFO)])
d.save("a0-04.agent-ports.svg")
