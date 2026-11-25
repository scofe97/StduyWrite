# a0-04 §1 사이드카의 포트가 향하는 두 방향.
# 본문(부록 D.1): 서비스용 다섯(15020 · 15021 · 15053 · 15001 · 15006)과 디버깅용 넷
#       (15000 · 15090 · 15004 · 15020). 15020 이 두 축에 걸친다. 15021 의 헬스 체크는
#       Envoy 가 15020 의 파일럿 에이전트로 넘겨 거기서 실제 판정이 일어난다.
# 타입 스펙: type-architecture — 두 경계(서비스용 · 사람용)와 포트 노드 간 연결을 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 636
d = D(W, H, "ISTIO IN ACTION · A0-04 §1",
      "여덟 포트가 두 방향으로 갈린다",
      "왼쪽은 다른 서비스를 향해 열린 다섯이고 오른쪽은 사람이 들여다보려고 열린 넷이다. "
      "15020 만 두 축에 걸쳐 있으며 15021 의 준비 확인은 15020 으로 넘어간다.",
      lead="15001 과 15006 은 iptables 리디렉션 규칙과 짝입니다")

def zone(x, y, w, h, label):
    d.t(x + 4, y - 10, label, 13, SOFT, KR, "start", 600)
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')

PW, PH = 360, 48
def port(x, y, num, what, focal=False, c=None):
    if focal:
        d.tone(x, y, PW, PH, ACC, 6, "12", 1.4)
    elif c:
        d.tone(x, y, PW, PH, c, 6, "12", 1.2)
    else:
        d.box(x, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 30, num, 14, ACC if focal else (c or INK), MONO, "start", 600)
    d.t(x + 88, y + 30, what, 13, MUTED, KR, "start")

zone(24, 148, 392, 404, "서비스를 향한 다섯")
zone(544, 148, 392, 320, "사람을 향한 넷")

LY = [168, 252, 324, 396, 468]
port(40, LY[0], "15020", "메트릭 · 헬스 체크", focal=True)
port(40, LY[1], "15021", "파드 준비 상태 확인")
port(40, LY[2], "15053", "로컬 DNS 프록시")
port(40, LY[3], "15001", "아웃바운드 리디렉션", c=INFO)
port(40, LY[4], "15006", "인바운드 리디렉션", c=INFO)

RY = [168, 240, 312, 384]
port(560, RY[0], "15000", "Envoy 관리 인터페이스")
port(560, RY[1], "15090", "Envoy 프록시 메트릭")
port(560, RY[2], "15004", "istiod 디버그 중계")
port(560, RY[3], "15020", "에이전트 디버그", focal=True)

# 15020 공유 점선 (x=452 세로선, 라벨은 오른쪽 x=464)
d.path("M 400 192 L 452 192 L 452 408 L 558 408", ACC, 1.5, m="acc", dash="5 4")
d.t(464, 292, "같은 포트", 13, ACC, KR, "start", 600)
d.t(464, 314, "두 축 겸용", 13, ACC, KR, "start", 600)

# 15021 -> 15020 판정 전달
d.arrow([(160, LY[1]), (160, LY[0] + PH + 2)], MUTED, "ar", 1.4)
d.t(176, LY[1] - 12, "판정 전달 (Envoy → 에이전트)", 13, SOFT, KR, "start")

d.legend(584, [("두 축에 걸친 포트", ACC), ("iptables 규칙과 짝인 포트", INFO)])
d.save("a0-04.agent-ports.svg")
print("ok a0-04.agent-ports")
