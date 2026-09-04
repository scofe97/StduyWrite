# a0-01 §6 도구 선택의 두 축.
# 본문(부록 A.4.2 끝): 권고는 istioctl 또는 istio-operator — 둘 다 IstioOperator API 를 쓰므로
#       입력 검증이 붙는다. 기업이 오퍼레이터로 기우는 이유는 "it is the GitOps approach and is
#       more fitting to their ideology" 인데, 저자는 "the operator adds complexity and requires
#       maintenance. Further, you can use istioctl and still adhere to the GitOps approach" 로
#       뒤집는다. GitOps 는 "operations of services and their configuration are sourced from a
#       Git repository. It doesn't matter what tool uses the configuration".
# 타입 스펙: type-quadrant — 두 축이 만드는 사분면에 도구를 놓는 것이 논점이다. 축 라벨은 양 끝에,
#           점은 이름과 한 줄 설명으로.
#           축약: 저자의 권고가 한 사분면에 몰리는 것이 결론이라 빈 사분면에 그 사실을 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, KR, MONO

W, H = 960, 672
d = D(W, H, "ISTIO IN ACTION · A0-01 §6",
      "검증이 붙는가와 컴포넌트를 더 세우는가",
      "가로축은 IstioOperator API 의 입력 검증이 붙는지이고 세로축은 클러스터에 컴포넌트를 더 "
      "세우는지다. 저자의 권고는 오른쪽 절반이고, 그 안에서 위아래는 감당할 복잡성의 문제다.",
      "GitOps 는 설정의 출처가 Git 이라는 뜻이지 도구 이름이 아닙니다")

CX, CY = 480, 320
AX0, AX1 = 120, 856
AY0, AY1 = 132, 508
d.path(f"M {AX0} {CY} L {AX1} {CY}", MUTED, 1.2, m="ar")
d.path(f"M {CX} {AY1} L {CX} {AY0}", MUTED, 1.2, m="ar")
d.t(AX0 - 12, CY + 4, "검증 없음", 12, INK, KR, "end", 600)
d.t(AX1 + 12, CY + 4, "검증 붙음", 12, INK, KR, "start", 600)
d.t(CX, AY0 - 12, "컴포넌트를 더 세운다", 12, INK, KR, "middle", 600)
d.t(CX, AY1 + 20, "세우지 않는다", 12, INK, KR, "middle", 600)

def dot(x, y, name, sub, focal=False):
    c = ACC if focal else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>')
    d.t(x + 16, y - 2, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 16, y + 18, sub, 11, MUTED, KR, "start")

dot(600, 200, "istio-operator", "GitOps 이념에 맞아 보이지만 유지 비용이 붙는다")
dot(600, 412, "istioctl", "같은 검증을 받고 컴포넌트는 늘지 않는다", focal=True)
dot(184, 412, "helm", "검증하는 층이 없다")

d.t(184, 196, "여기는 비어 있다", 12, SOFT, KR, "start", 600)
d.t(184, 218, "검증도 없이 컴포넌트만 늘릴 이유가 없다", 11, MUTED, KR, "start")

BY = 500
d.t(28, BY + 60, "저자의 권고는 오른쪽 절반 — 둘 다 IstioOperator API 를 쓰므로 입력 검증이 한 겹 더 붙는다", 11, ACC, KR, "start", 600)
d.t(28, BY + 84, "기업이 위쪽으로 기우는 이유를 저자는 이념이라 적고 곧바로 뒤집는다. 오퍼레이터는 복잡성을 더하고 유지보수를 요구한다", 11, SOFT, KR, "start")
d.t(28, BY + 108, "GitOps 는 서비스와 설정의 운영이 Git 저장소에서 나온다는 뜻일 뿐이고 무엇이 그 설정을 소비하는지는 상관없다", 11, MUTED, KR, "start")
d.legend(BY + 128, [("저자가 기본으로 두는 자리", ACC), ("나머지 자리", MUTED)])
d.save("a0-01.tool-choice.svg")
