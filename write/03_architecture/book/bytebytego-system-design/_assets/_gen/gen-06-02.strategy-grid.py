# 타입 스펙: type-dp-security-matrix — 배포 전략 다섯 행 × 진행 단계 다섯 열의 비교 행렬(격자 문법). 칸마다 새 버전을 받는 비율을 막대로 보이고, 초점 칸 하나는 카나리의 처음 10%.
# 사실 출처: 다중 서비스 동시 배포 = 추출본 v1.txt 837~851행과 쪽 31 그림(서비스 A~D 가 한 번에 올라감)
#   · 롤링 = Kubernetes v1.37 Deployment 문서(v1.35 문서와 같은 문장) "Rolling Update Deployment"(maxUnavailable·maxSurge 기본 25%, 서버 4대·한 대씩 교체는 이 편이 정한 설계 가정이라 25·50·75·100%)
#   · 블루그린 = Martin Fowler "BlueGreenDeployment"(두 환경 사이 라우터를 한 번에 전환)
#   · 카나리 = AWS CodeDeploy "CodeDeployDefault.LambdaCanary10Percent5Minutes"(처음 10%, 5분 뒤 나머지 90%)
#   · 특성 토글 = Pete Hodgson "Feature Toggles"(martinfowler.com)(Release Toggles 는 코드를 먼저 배포하고 켜는 시점을 따로 정함, 켜기 전 0% 와 켠 뒤 100% 는 정의 그대로).
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 208, 단계 열 폭 120·간격 12, header_h 36, header_y 96, row_h 48 · stride 56. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, COL_W, COL_GAP = 12, 208, 12, 120, 12
HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 96, 36, 144, 48, 56
NSTEP = 5
rows = [
    ("다중 서비스 동시", "서비스 A~D 한꺼번에", [0, 100]),
    ("롤링", "서버 4대를 한 대씩", [0, 25, 50, 75, 100]),
    ("블루그린", "환경 두 벌 + 라우터", [0, 100]),
    ("카나리", "10% → 5분 뒤 100%", [0, 10, 100]),
    ("특성 토글", "코드 100% 먼저, 노출은 따로", [0, 100]),
]
FOCAL = (3, 1)

W = LEFT + COMP_W + GAP0 + NSTEP * COL_W + (NSTEP - 1) * COL_GAP + 48
H = ROW0 + (len(rows) - 1) * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 06-02 §1",
      "전략마다 새 버전이 퍼지는 속도",
      "새 버전을 받는 비율이 단계마다 어떻게 늘어나는지를 한 격자에 놓았습니다",
      "롤링 행은 서버 4대를 한 대씩 바꾼다고 가정합니다")


def cx(j):
    return LEFT + COMP_W + GAP0 + j * (COL_W + COL_GAP)


d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 23, "전략 × 단계", 12, INK, KR, "middle", 600)
for j in range(NSTEP):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 23, str(j + 1), 13, INK, MONO, "middle", 600)

TRACK = COL_W - 24
for i, (name, sub, shares) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 20, name, 13, INK, KR, "start", 600)
    d.t(LEFT + 12, y + 38, sub, 12, MUTED, KR, "start")
    for j, s in enumerate(shares):
        x = cx(j)
        focal = (i, j) == FOCAL
        if focal:
            d.tone(x, y, COL_W, ROW_H, ACC, 4, "14", 1.4)
        else:
            d.box(x, y, COL_W, ROW_H, PAPER2, RULE, 0.9, 4)
        col = ACC if focal else OK
        d.t(x + COL_W / 2, y + 20, f"{s}%", 12, col, MONO, "middle", 600)
        d.o.append(f'<rect x="{x + 12}" y="{y + 30}" width="{TRACK}" height="8" rx="2" fill="{INFO}33"/>')
        if s > 0:
            d.o.append(f'<rect x="{x + 12}" y="{y + 30}" width="{TRACK * s / 100}" height="8" rx="2" fill="{col}"/>')

d.legend(H - 44, [("새 버전 비율", OK), ("이전 버전", INFO), ("처음 노출", ACC)])
d.save("06-02.strategy-grid.svg")
