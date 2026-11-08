# 04-04.chapter-overview — 04-04 의 키워드 개념도. 본문 ## 여덟 묶음을 노드와 주소 · 서비스 · 정책과 이름 · 경계 밖 네 구역에 잇는다.
# 본문 요구: `## 학습 목표` 아래 지도 — 묶음 1~8 이 어느 구역에 속하고 어떤 값을 짚는지 한눈에 보인다.
#           노드와 주소(1·2), 서비스(3·4), 정책과 이름(5·6·7), 경계 밖(8).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 노드 격자, 화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 구역.
#           focal 은 "선택 → 방향 잠금" 노드 하나(묶음 5). 노드 부제는 본문에서 실제로 본 값이다.
import ddx
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 100, 320, 216, 64
ROW_Y, ROW_STRIDE = 112, 112
W, H = 1000, 640


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-04 OVERVIEW",
      "여덟 묶음은 노드에서 시작해 노드 밖에서 끝납니다",
      "04-04 의 키워드 개념도. 첫 줄은 CNI 가 없는 노드가 멈추고 Cilium 이 설치되면 주소 대역이 노드 조각으로 내려오는 흐름이다. "
      "둘째 줄은 서비스 하나가 만드는 규칙 11줄과 readiness 를 잃은 Pod 의 줄이 사라지는 흐름이다. "
      "셋째 줄은 정책이 Pod 를 선택해 잠그고 이름 하나가 질의를 불리고 Cilium L7 정책이 응답 서명을 가르는 흐름이다. "
      "넷째 줄은 노드 밖에서 Pod 로 가는 길이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 구역입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "1F" if c == ACC else "14", 1.6 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, ddx.fit(title, 13, NW - 16, title), 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, ddx.fit(sub, 12, NW - 16, sub), 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, ddx.fit(label, 12, x2 - x1 - 8, label), 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 24
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


def drop(i, j, label):
    # 한 줄이 한두 노드로 끝날 때: 마지막 노드 아래에서 다음 줄 첫 노드 위로
    xa, xb = nx(j) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 24
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("노드와 주소", "서비스", "정책과 이름", "경계 밖")):
    d.chip(48, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "CNI 없는 클러스터", "노드 셋 NotReady", WARN)
node(0, 1, "주소 재고", "10.244.0.0/16 → 노드별 /24", INFO)
harrow(0, 0, "설치하면")
drop(0, 1, "주소가 생겼으니")

node(1, 0, "서비스 하나의 줄", "default/web 11줄", INFO)
node(1, 1, "readiness 이탈", "낙하 9.9초 · 복귀 3.3초", INFO)
harrow(1, 0, "Pod 가 빠지면")
drop(1, 1, "서비스 위에 정책을")

node(2, 0, "선택되는 순간의 잠금", "규칙 0줄도 000", ACC)
node(2, 1, "이름 하나의 질의", "getent 2 · 8 · 2 · 8", OK)
node(2, 2, "Cilium L7 정책", "200 · 403 · 000", INFO)
harrow(2, 0, "이름도 막히면")
harrow(2, 1, "경로까지 보려면")
wrap(2, "클러스터 경계 밖에서는")

node(3, 0, "노드 밖에서 Pod 로", "masquerade · 경로 직접 추가", WARN)

d.legend(570, [("멈춤·함정", WARN), ("구조·값", INFO), ("방향이 잠기는 순간", ACC), ("이름 질의", OK)])
d.save("04-04.chapter-overview.svg")
print("ok chapter-overview")
