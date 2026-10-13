# 타입 스펙: type-flowchart — 원본 영상 하나가 단계 1(영상·오디오·메타데이터)과 단계 2(영상 인코딩·썸네일·오디오 인코딩)로 잘린다. 점선이 단계 경계이고 간선은 수평·수직 직각이다.
# 사실 출처: 추출본 v2.txt 4126~4135행(DAG 스케줄러가 DAG 를 단계로 나눠 작업 큐에 넣는다. 단계 1: 영상·오디오·메타데이터, 단계 2: 영상 인코딩·썸네일·오디오 인코딩), PDF 233쪽 그림.
#   그림에서 메타데이터에는 이어지는 작업이 없다. funny.mov 는 14-01 편의 예시 이름이다. "작업 3 개" 는 각 단계 칸의 노드를 센 값이다.
# Layout conventions: 노드 높이 56, 타원 높이 48, 열 x = 24(원본)·340(단계 1)·700(단계 2), 노드 폭 160, 단계 경계 점선 x=300·660. 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, RULE, KR, MONO

W, H = 960, 520
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-02 §2",
      "같은 단계의 작업 사이에는 간선이 없어 서로 기다리지 않는다",
      "원본에서 간선 한 개로 닿는 영상·오디오·메타데이터가 단계 1, 영상에서 이어지는 영상 인코딩·썸네일과 오디오에서 이어지는 오디오 인코딩이 단계 2 다.",
      "점선이 단계 경계 · 같은 단계의 작업 사이에는 간선이 없다")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def rect(x, y, w, h, title, sub, c, r=6):
    d.tone(x, y, w, h, c, r, "12", 1.1)
    d.t(x + w / 2, y + h / 2 + 5, title, 13, INK, fam(title), "middle", 600)


NW, NH = 160, 56
# 단계 경계
for x in (300, 660):
    d.line(x, 100, x, 452, SOFT, 1.0, "4 6")
d.t(340 + NW / 2, 124, "단계 1 · 작업 3 개", 13, SOFT, KR, "middle", 600)
d.t(700 + NW / 2, 124, "단계 2 · 작업 3 개", 13, SOFT, KR, "middle", 600)

# 원본 — 오디오와 같은 높이(mid y=320)에 두고 단계 1 의 세 노드로 버스를 편다
d.o.append(f'<rect x="24" y="296" width="200" height="48" rx="24" fill="{INFO}12" stroke="{INFO}" stroke-width="1.1"/>')
d.t(124, 316, "원본 영상", 13, INK, KR, "middle", 600)
d.t(124, 334, "funny.mov", 11, MUTED, MONO)

Y1 = (176, 292, 388)  # 영상 · 오디오 · 메타데이터
BUS_X = 272
d.line(224, 320, BUS_X, 320, MUTED, 1.4)
d.line(BUS_X, Y1[0] + NH // 2, BUS_X, Y1[2] + NH // 2, MUTED, 1.4)
for y, nm in zip(Y1, ("영상", "오디오", "메타데이터")):
    d.arrow([(BUS_X, y + NH // 2), (340 - 6, y + NH // 2)], MUTED, "ar", 1.4)
    rect(340, y, NW, NH, nm, "", INFO)

# 단계 2 — 영상에서 둘, 오디오에서 하나
Y2 = {"영상 인코딩": 140, "썸네일": 212}
BUS2 = 620
d.line(340 + NW + 2, Y1[0] + NH // 2, BUS2, Y1[0] + NH // 2, MUTED, 1.4)
d.line(BUS2, Y2["영상 인코딩"] + NH // 2, BUS2, Y2["썸네일"] + NH // 2, MUTED, 1.4)
for nm, y in Y2.items():
    d.arrow([(BUS2, y + NH // 2), (700 - 6, y + NH // 2)], MUTED, "ar", 1.4)
    rect(700, y, NW, NH, nm, "", OK)
d.arrow([(340 + NW + 2, Y1[1] + NH // 2), (700 - 6, Y1[1] + NH // 2)], MUTED, "ar", 1.4)
rect(700, Y1[1], NW, NH, "오디오 인코딩", "", OK)

d.legend(H - 56, [("원본과 단계 1", INFO), ("단계 2 작업", OK)])
d.save("14-02.dag-stages.svg")
