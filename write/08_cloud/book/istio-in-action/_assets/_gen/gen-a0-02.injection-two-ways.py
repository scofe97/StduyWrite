# a0-02 §2 주입의 두 길.
# 본문(부록 B.1): 수동은 istioctl kube-inject -f deployment.yaml, 자동은 mutating admission
#       webhook. "The modifications are the same as when using istioctl."
#       프로토타이핑이면 kubectl apply 로 파이프, 운영이면 정의를 갱신해 Git 에 두고 CD 가 적용.
# 타입 스펙: type-swimlane — 같은 결과에 이르는 두 경로를 주체별 레인으로 갈라 놓는 것이 논점이다.
#           레인마다 단계를 시간 순으로 놓고 끝에서 합류시킨다.
#           축약: accent 는 두 경로가 같은 것을 낸다는 합류점 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 520
d = D(W, H, "ISTIO IN ACTION · A0-02 §2",
      "손으로 넣든 웹훅이 넣든 결과는 같다",
      "위 레인은 사람이 istioctl 로 명세를 고치는 길이고 아래 레인은 웹훅이 대신 고치는 길이다. "
      "색이 붙은 칸이 두 길이 같은 것을 낸다는 저자의 문장이 서는 자리다.",
      "갈리는 것은 결과가 아니라 무엇이 배포되는지를 얼마나 통제하느냐입니다")

LANE_H, LANE_Y0 = 116, 132
lanes = [("수동 주입", "사람이 명령을 친다"), ("자동 주입", "웹훅이 대신 넣는다")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 50, name, 12, INK, KR, "start", 600)
    d.t(20, top + 70, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(164, LANE_Y0, 164, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 172, 68
# 칸 넷이 1044 까지 나갔다. 폭 172 · 간격 32 로 줄여 972 에서 끝나게 한다.
def sx(j): return 188 + j * 204
def sy(k): return LANE_Y0 + k * LANE_H + 24
def cell(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 28, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 48, sub, 11, MUTED, KR, "middle")

cell(0, 0, "평범한 명세", "부품이 하나도 없다")
cell(0, 1, "istioctl kube-inject", "부품을 적어 넣는다")
cell(0, 2, "고쳐진 명세", "사람이 결과를 본다")
cell(1, 0, "평범한 명세", "그대로 둔다")
cell(1, 1, "kubectl apply", "명세를 그냥 올린다")
cell(1, 2, "웹훅이 가로챈다", "저장되기 전에 고친다")
cell(0, 3, "같은 파드 정의", "컨테이너 둘 + init 하나", focal=True)

for k in (0, 1):
    for j in (0, 1):
        d.arrow([(sx(j) + SW, sy(k) + SH / 2), (sx(j + 1) - 2, sy(k) + SH / 2)], MUTED, "ar", 1.4)
JX = sx(3) - 24
d.path(f"M {sx(2) + SW} {sy(0) + SH / 2} L {JX} {sy(0) + SH / 2}", ACC, 1.5)
d.path(f"M {sx(2) + SW} {sy(1) + SH / 2} L {JX} {sy(1) + SH / 2}", ACC, 1.5)
d.path(f"M {JX} {sy(1) + SH / 2} L {JX} {sy(0) + SH / 2}", ACC, 1.5)
d.arrow([(JX, sy(0) + SH / 2), (sx(3) - 2, sy(0) + SH / 2)], ACC, "acc", 1.5)

d.t(28, 404, "프로토타이핑이면 출력을 kubectl apply 로 흘려보낸다 — 책 전체가 그렇게 한다", 11, SOFT, KR, "start")
d.t(28, 428, "운영이면 서비스마다 정의를 갱신해 Git 에 두고 지속적 배포 파이프라인이 적용한다", 11, MUTED, KR, "start")
d.legend(452, [("두 길이 같은 것을 내는 자리", ACC), ("각 길의 단계", MUTED)])
d.save("a0-02.injection-two-ways.svg")
