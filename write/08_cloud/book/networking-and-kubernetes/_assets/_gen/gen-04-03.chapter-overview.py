# 04-03.chapter-overview — 04-03 의 키워드 개념도. 본문 정리의 ### 열두 개를 잠금 · 문법 · 이름 · 처방과 주소 네 묶음으로 4행 × 3열에 잇는다.
# 본문 요구: 핵심 요약의 "NetworkPolicy 는 Pod 가 선택되는 순간부터 방향마다 허용 목록의 연결만 통과시키는 방화벽"
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자, 화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 묶음.
#           focal 은 "선택 → 방향 잠금" 노드 하나. 2026-11-08 새 ### 배치에 맞춰 다시 그렸다.
import ddx
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 100, 320, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 1000, 664


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-03 OVERVIEW",
      "정책은 선택되는 순간 잠그고 이름은 검색 경로 때문에 불어납니다",
      "04-03 의 키워드 개념도. 첫 줄은 정책이 Pod 를 선택해 방향을 잠그고 세 단계로 조여 가며 CNI 가 라벨을 주소로 번역하는 흐름이다. "
      "둘째 줄은 LabelSelector 연산자 넷과 peer 의 AND·OR 를 거쳐 ClusterNetworkPolicy 같은 확장으로 넘어가는 흐름이다. "
      "셋째 줄은 dnsPolicy 가 정한 resolv.conf 의 검색 경로가 이름 하나의 질의를 불리고 클라이언트마다 횟수가 갈리는 흐름이다. "
      "넷째 줄은 처방 셋과 ipFamilyPolicy 기본값, 전환 규칙으로 닫는 흐름이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 묶음입니다.")


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
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("잠금", "문법", "이름", "처방·주소")):
    d.chip(48, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "선택 → 방향 잠금", "policyTypes 방향마다", ACC)
node(0, 1, "세 단계 조이기", "규칙 0줄도 양방향 차단", INFO)
node(0, 2, "라벨 → 주소 번역", "CNI 가 커널로", WARN)
harrow(0, 0, "예외는")
harrow(0, 1, "강제는")
wrap(0, "무엇을 고르나")

node(1, 0, "LabelSelector", "연산자 넷", INFO)
node(1, 1, "peer 의 AND·OR", "대시 하나 차이", WARN)
node(1, 2, "표준 밖의 확장", "L7 · ClusterNetworkPolicy", OK)
harrow(1, 0, "대상을 골라")
harrow(1, 1, "한계 너머")
wrap(1, "이름 쪽으로")

node(2, 0, "dnsPolicy", "ClusterFirst 가 기본", INFO)
node(2, 1, "검색 경로", "ndots:5 · 최대 시도 4번", WARN)
node(2, 2, "클라이언트별 횟수", "web 질의 2에서 5까지", OK)
harrow(2, 0, "resolv.conf")
harrow(2, 1, "리졸버마다")
wrap(2, "비용을 줄이려면")

node(3, 0, "처방 셋", "끝점 · ndots · Autopath", OK)
node(3, 1, "ipFamilyPolicy", "SingleStack 이 기본", INFO)
node(3, 2, "전환 규칙", "primary 불변", WARN)
harrow(3, 0, "주소 계열은")
harrow(3, 1, "바꿀 때")

d.legend(600, [("구조·흐름", INFO), ("한계·함정", WARN), ("방향이 잠기는 순간", ACC), ("확장·처방", OK)])
d.save("04-03.chapter-overview.svg")
print("ok 04-03 overview")
