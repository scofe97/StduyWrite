# 01-01 §6 ESB · API 게이트웨이 · 서비스 메시가 놓이는 자리.
# 본문: ESB 는 배포와 구현이 고도로 중앙집중적이었고 애플리케이션 네트워킹과 서비스 중재 관심사를 섞었다.
#       서비스 메시의 역할은 애플리케이션 네트워킹 관심사에 한정된다 — 비즈니스 변환·프로세스 오케스트레이션·
#       예외 처리·서비스 오케스트레이션은 메시에 속하지 않는다.
#       API 게이트웨이는 내부 API 에 쓸 때 홉이 두 번 생기고 중앙 병목이 된다.
# 타입 스펙: type-quadrant — 2x2. 축 라벨은 팁마다 한 단어(화살표 글리프·괄호 금지), 항목은 r=4 점 + 라벨,
#           초점 하나(coral). 항목이 축선을 걸치지 않게 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, RULE, KR, MONO

W, H = 1000, 660
d = D(W, H, "ISTIO IN ACTION · 01-01 §6",
      "범위를 좁히고 자리를 흩는다",
      "가로축은 어디에 배치되는가, 세로축은 무엇까지 맡는가. 저자가 ESB 를 인용문으로 소환해 같은 점과 "
      "다른 점을 가르는 대목이 이 두 축이다. 색이 붙은 것이 이 책이 고른 자리다.",
      "ESB 는 새 사일로를 만들었고 그 조직이 통합의 문지기가 됐습니다")

CX, CY = 500, 356
AX0, AX1 = 176, 864
AY0, AY1 = 164, 536

d.path(f"M {CX} {AY1} L {CX} {AY0}", INK, 1.2, m="ar")
d.path(f"M {AX0} {CY} L {AX1} {CY}", INK, 1.2, m="ar")
d.line(CX, AY1, CX, CY, INK, 1.2)
d.line(AX0, CY, CX, CY, INK, 1.2)

d.t(CX, AY0 - 14, "중재까지", 11, INK, MONO, "middle", 400)
d.t(CX, AY1 + 22, "네트워킹만", 11, INK, MONO, "middle", 400)
d.t(AX0 - 14, CY + 4, "중앙", 11, INK, MONO, "end", 400)
d.t(AX1 + 14, CY + 4, "분산", 11, INK, MONO, "start", 400)

def item(x, y, name, sub, focal=False, anchor="start", dx=14):
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
    d.t(x + dx, y - 3, name, 13, ACC if focal else INK, KR, anchor, 600)
    d.t(x + dx, y + 14, sub, 9, MUTED, MONO, anchor)

item(288, 232, "ESB", "silo · single point")
item(304, 452, "API gateway", "extra hop per service")
item(672, 468, "service mesh", "sidecar · no extra hop", focal=True)

d.t(188, 188, "중앙에서 비즈니스까지", 11, SOFT, KR, "start")
d.t(812, 188, "분산인데 중재까지 — 비어 있다", 11, SOFT, KR, "end")
d.t(188, 512, "중앙에서 네트워킹만", 11, SOFT, KR, "start")
d.t(812, 512, "분산에서 네트워킹만", 11, SOFT, KR, "end")

d.t(32, 580, "메시가 맡지 않는 것 — X12·EDI·HL7 변환 · 비즈니스 프로세스 오케스트레이션 · 예외 처리 · 서비스 오케스트레이션", 11, SOFT, KR, "start")
d.legend(604, [("이 책이 고른 자리", ACC), ("앞선 기술", MUTED)])
d.save("01-01.esb-gateway-mesh.svg")
