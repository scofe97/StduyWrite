# 06-02 §3 — 스캐폴딩이 한 번에 심는 것 (원문 Frictionless Micro-Frontend Blueprints).
# 레인이 역할이고 열이 단계다. 점선은 플랫폼 쪽이 등록해 둔 것이 스캐폴딩 실행에 끌려 들어오는 경로다.
# 타입 스펙: type-data-flow — 파이프라인 단계마다 누가 무엇을 하는지. 역할 레인 × 단계 열 격자.
#           §1 입력 계약: lanes 2 · steps 4 · focal 1. 축약: payload 칩(in/out)은 이 절의 논지가 아니라 생략하고
#           대신 각 노드에 도구 줄을 남겼다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
LABX, LABW = 12, 188
X0, CW, CGAP = 216, 220, 32
HDR_Y, HDR_H = 112, 36
LANE_Y0, LANE_H = 168, 140
NH = 96
LEGEND_Y = LANE_Y0 + 2 * LANE_H + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-02 §3",
      "스캐폴딩이 한 번에 심는 것",
      "위 레인이 표준을 등록해 두는 쪽이고 아래가 그것을 받아 시작하는 쪽이다. 색이 붙은 단계에서 명령 하나가 둘을 합친다.",
      "점선은 미리 등록해 둔 것이 스캐폴딩에 끌려 들어오는 경로입니다")

steps = [("01", "청사진 등록"), ("02", "자동화 표본"), ("03", "스캐폴딩 실행"), ("04", "첫 코드")]
FOCAL_STEP = 2
lanes = [("플랫폼 · DX 팀", "PLT"), ("개발 팀", "DEV")]

def sx(j): return X0 + j * (CW + CGAP)

# 단계 머리글
for j, (num, label) in enumerate(steps):
    x = sx(j)
    if j == FOCAL_STEP:
        d.o.append(f'<rect x="{x}" y="{HDR_Y}" width="{CW}" height="{HDR_H}" rx="6" fill="{ACC}" />')
        d.t(x + CW / 2, HDR_Y + 23, f"{num}  {label}", 11, PAPER, KR, "middle", 600)
    else:
        d.box(x, HDR_Y, CW, HDR_H, PAPER2, RULE, 0.9, 6)
        d.t(x + CW / 2, HDR_Y + 23, f"{num}  {label}", 11, INK, KR, "middle", 600)

# 레인 구분선
for i in range(3):
    d.line(LABX, LANE_Y0 + i * LANE_H, W - 48, LANE_Y0 + i * LANE_H, RULE, 0.8)
for li, (name, key) in enumerate(lanes):
    ly = LANE_Y0 + li * LANE_H
    d.t(LABX + 12, ly + LANE_H / 2 - 2, name, 12.5, INK, KR, "start", 600)
    d.t(LABX + 12, ly + LANE_H / 2 + 18, key, 9, SOFT, MONO, "start")

nodes = [
    (0, 0, "청사진과 표본", "모범 사례와 가드레일을 모은다", "중앙 포털 · Backstage", False),
    (0, 1, "자동화 표본", "정적 분석 · 보안 테스트 설정", "핵심 단계가 담긴 표본", False),
    (1, 2, "명령 하나로 골격", "의존성과 표준이 함께 들어온다", "스캐폴딩 CLI", True),
    (1, 3, "코드를 쓰기 시작", "표준이 제자리에 놓인 채 출발", "관측 · 로깅이 이미 있다", False),
]
POS = {}
for li, sj, title, sub, tool, focal in nodes:
    x, y = sx(sj), LANE_Y0 + li * LANE_H + (LANE_H - NH) / 2
    POS[(li, sj)] = (x, y)

# 연결선 먼저 — z-order
def edge(a, b, c, dash=None):
    (x1, y1), (x2, y2) = POS[a], POS[b]
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + NH / 2), (x2 - 2, y2 + NH / 2)], c, "acc" if c == ACC else "ar", 1.3, dash)
    else:
        d.arrow([(x1 + CW / 2, y1 + NH), (x1 + CW / 2, y2 - 18), (x2 + CW / 2, y2 - 18), (x2 + CW / 2, y2 - 2)],
                c, "ar", 1.2, dash)

edge((0, 0), (0, 1), MUTED)
edge((0, 0), (1, 2), SOFT, "4 4")
edge((0, 1), (1, 2), SOFT, "4 4")
edge((1, 2), (1, 3), ACC)

for li, sj, title, sub, tool, focal in nodes:
    x, y = POS[(li, sj)]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 28, title, 12, ACC if focal else INK, KR, "start", 600)
    d.t(x + 14, y + 50, sub, 9.5, MUTED, KR, "start")
    d.t(x + 14, y + 74, tool, 8.5, SOFT, MONO, "start")

d.legend(LEGEND_Y, [("명령 하나가 둘을 합치는 자리", ACC), ("미리 등록해 둔 것이 끌려온다", SOFT)])
d.save("06-02.scaffolding.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", sx(3) + CW)
