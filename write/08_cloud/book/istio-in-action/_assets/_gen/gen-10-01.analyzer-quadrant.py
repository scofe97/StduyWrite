# 10-01 §3 자동 분석기 셋이 서는 자리.
# 본문 근거(원문 10.2.3): "The istioctl analyze command ... can be run on clusters that are already
#       experiencing issues or can validate configurations before they are applied to clusters to prevent
#       misconfiguring resources in the first place." → 가로축(사전 · 사후)이 여기서 나온다.
#       describe 는 "the workload-specific configuration" 을 요약한다 → 세로축(넓게 · 좁게).
# 왼쪽 아래 칸은 비어 있다 — 적용 전에 워크로드 하나로 좁혀 보는 도구를 저자가 들지 않는다.
# 타입 스펙: type-quadrant — 2x2 격자. 축 라벨은 팁마다 한 단어(Jobs-minimal, 화살표 글리프 · 괄호 금지),
#           항목은 r=4 점 + 라벨, 초점 하나, 항목이 축선을 걸치지 않게 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 10-01 §3",
      "같은 오류를 셋이 다른 자리에서 잡는다",
      "가로축은 언제 보는가, 세로축은 얼마나 넓게 보는가. 셋 다 subset 이 없다는 같은 사실을 알려 주지만 "
      "서는 자리가 다르다. 색이 붙은 것만 클러스터에 넣기 전에 막을 수 있다.",
      "왼쪽 아래는 비어 있습니다 — 적용 전에 워크로드 하나로 좁혀 보는 도구는 없습니다")

CX, CY = 500, 340
AX0, AX1 = 176, 824
AY0, AY1 = 152, 520

d.path(f"M {CX} {AY1} L {CX} {AY0}", INK, 1.2, m="ar")
d.path(f"M {AX0} {CY} L {AX1} {CY}", INK, 1.2, m="ar")
d.line(CX, AY1, CX, CY, INK, 1.2)
d.line(AX0, CY, CX, CY, INK, 1.2)

d.t(CX, AY0 - 14, "넓게", 9, INK, MONO, "middle", 400)
d.t(CX, AY1 + 22, "좁게", 9, INK, MONO, "middle", 400)
d.t(AX0 - 14, CY + 4, "사전", 9, INK, MONO, "end", 400)
d.t(AX1 + 14, CY + 4, "사후", 9, INK, MONO, "start", 400)

def item(x, y, name, sub, focal=False, dx=14, anchor="start"):
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
    d.t(x + dx, y - 3, name, 13, ACC if focal else INK, KR, anchor, 600)
    d.t(x + dx, y + 14, sub, 9, MUTED, MONO, anchor)

item(280, 216, "적용 전 파일 검증", "istioctl analyze <file>", focal=True)
item(596, 200, "Kiali 설정 검증", "KIA1107 subset not found")
item(624, 288, "네임스페이스 분석", "istioctl analyze -n <ns>")
item(628, 440, "워크로드 요약", "istioctl x describe pod")

d.t(196, 176, "고치기 전에 막는다", 10, SOFT, KR, "start")
d.t(804, 176, "이미 난 문제를 훑는다", 10, SOFT, KR, "end")
d.t(196, 500, "이 자리에 도구가 없다", 10, SOFT, KR, "start")
d.t(804, 500, "한 워크로드로 좁힌다", 10, SOFT, KR, "end")

d.t(32, 560, "describe 는 파드가 이미 떠 있어야 답한다 — 그래서 사전 쪽으로 오지 못한다", 11, SOFT, KR, "start")
d.legend(584, [("클러스터에 넣기 전에 막는 자리", ACC), ("난 뒤에 훑는 자리", MUTED)])
d.save("10-01.analyzer-quadrant.svg")
