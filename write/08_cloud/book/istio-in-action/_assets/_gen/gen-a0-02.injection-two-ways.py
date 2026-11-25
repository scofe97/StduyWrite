# a0-02 §2 주입의 두 길.
# 값 근거(본문 §2 · 부록 B.1):
#   - 평범한 명세: httpbin Deployment (port 80).
#   - 수동: istioctl kube-inject -f deployment.yaml (프로토타입은 kubectl apply, 운영은 Git + CD).
#   - 자동: kubectl apply 로 그대로 올리면 웹훅이 저장 전 주입.
#   - 결과 동일: 컨테이너 둘(app + istio-proxy) + initContainers(istio-init).
# 타입 스펙: type-swimlane — 같은 결과에 이르는 두 경로를 레인으로 갈라 합류시킨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 460
d = D(W, H, "ISTIO IN ACTION · A0-02 §2",
      "손으로 넣든 웹훅이 넣든 결과는 같다",
      "위 레인은 사람이 istioctl 로 명세를 고치는 길이고 아래 레인은 웹훅이 대신 고치는 길이다. "
      "코랄색 칸이 두 길이 같은 파드 정의를 낸다는 합류점이다.",
      lead="갈리는 것은 결과가 아니라 무엇이 배포되는지를 Git 에서 얼마나 통제하느냐입니다.")

LANE_H, LANE_Y0 = 120, 116
lanes = [("수동 주입", "istioctl 실행"), ("자동 주입", "웹훅이 대신 넣음")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 50, name, 14, INK, KR, "start", 600)
    d.t(20, top + 74, sub, 13, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(152, LANE_Y0, 152, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 172, 72
def sx(j): return 176 + j * 196
def sy(k): return LANE_Y0 + k * LANE_H + 24

def cell(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.tone(x, y, SW, SH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    fam = KR if any("가" <= c <= "힣" for c in label) else MONO
    d.t(x + SW / 2, y + 28, label, 13, ACC if focal else INK, fam, "middle", 600)
    d.t(x + SW / 2, y + 52, sub, 13, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")


cell(0, 0, "평범한 명세", "httpbin · port 80")
cell(0, 1, "istioctl kube-inject", "부품을 적어 넣는다")
cell(0, 2, "고쳐진 명세", "Git · kubectl apply")
cell(1, 0, "평범한 명세", "Deployment 그대로 둠")
cell(1, 1, "kubectl apply", "명세를 그냥 올린다")
cell(1, 2, "웹훅이 가로챈다", "저장 전 파드만 수정")
cell(0, 3, "같은 파드 정의", "컨테이너 2 + init 1", focal=True)

for k in (0, 1):
    for j in (0, 1):
        d.arrow([(sx(j) + SW, sy(k) + SH / 2), (sx(j + 1) - 2, sy(k) + SH / 2)], MUTED, "ar", 1.4)

JX = sx(3) - 20
d.path(f"M {sx(2) + SW} {sy(0) + SH / 2} L {JX} {sy(0) + SH / 2}", ACC, 1.5)
d.path(f"M {sx(2) + SW} {sy(1) + SH / 2} L {JX} {sy(1) + SH / 2}", ACC, 1.5)
d.path(f"M {JX} {sy(1) + SH / 2} L {JX} {sy(0) + SH / 2}", ACC, 1.5)
d.arrow([(JX, sy(0) + SH / 2), (sx(3) - 2, sy(0) + SH / 2)], ACC, "acc", 1.5)

d.legend(392, [("두 길이 같은 것을 내는 자리", ACC), ("각 길의 단계", MUTED)])
d.save("a0-02.injection-two-ways.svg")
print("ok injection-two-ways")
