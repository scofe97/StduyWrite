# 20-01 개념도 — 스레드는 한 주소 공간 안에 실행 지점을 여럿 두며, 공유 데이터 접근에서 경쟁 상태가 생겨 임계 구역과 상호 배제가 필요해진다.
# 본문 요구(20-01 「학습 목표」 개념도 문단): 1행 스레드·주소 공간 공유·스택 분리(§1), 2행 병렬성·입출력 겹치기·스레드를 쓰는 이유(§2),
#           3행 생성 순서·스케줄러·비결정성(§3), 4행 공유 카운터·경쟁 상태·잃어버린 갱신(§4), 5행 임계 구역·상호 배제·원자성(§5), 6행 동기화 기본 요소·조건 변수·다음 장들(§5).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 26장 §26.1~§26.5 (VERSION 1.10).
# 타입 스펙: type-architecture — 키워드 개념도. 6행 × 3열 노드 격자(04-01 개념도와 같은 공식: 열 x = 60 + j·340, 노드 216×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 104
W, H = 984, 780


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 20-01 OVERVIEW",
      "스레드는 주소 공간을 나눠 쓰므로 공유 데이터 앞에서 동기화가 필요해진다",
      "20-01 의 키워드 개념도. 1행은 스레드가 한 주소 공간을 함께 쓰되 스택은 따로 가진다는 정의다. "
      "2행은 병렬성과 입출력 겹치기가 스레드를 쓰는 두 이유라는 점이다. "
      "3행은 스레드 실행 순서를 스케줄러가 정하므로 결과가 실행마다 달라진다는 점이다. "
      "4행은 공유 카운터를 읽고 더하고 쓰는 사이에 전환이 끼어들면 갱신이 사라지는 경쟁 상태다. "
      "5행은 그 구간을 임계 구역으로 보고 한 번에 한 스레드만 들이는 상호 배제다. "
      "6행은 이를 위해 하드웨어와 운영체제가 동기화 기본 요소를 제공하고, 기다림은 조건 변수가 맡는다는 예고다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 13, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "스레드", "실행 지점이 여럿", INFO)
node(0, 1, "주소 공간 공유", "코드·힙·전역 변수", INFO)
node(0, 2, "스레드마다 스택", "PC·레지스터도 따로", OK)
harrow(0, 0, "한 프로세스 안에서")
harrow(0, 1, "다만")

node(1, 0, "병렬성", "CPU 마다 한 스레드", INFO)
node(1, 1, "입출력 겹치기", "기다리는 동안 계산", INFO)
node(1, 2, "스레드를 쓰는 이유", "데이터 공유가 쉬움", OK)
harrow(1, 0, "그리고")
harrow(1, 1, "둘 다")

node(2, 0, "스레드 생성", "함수 호출과 닮음", INFO)
node(2, 1, "스케줄러", "다음에 돌 쪽을 정함", INFO)
node(2, 2, "실행 순서 비결정", "A 먼저도 B 먼저도", WARN)
harrow(2, 0, "생성 뒤엔")
harrow(2, 1, "순서를 모르니")

node(3, 0, "공유 카운터", "읽기·더하기·쓰기", INFO)
node(3, 1, "중간에 전환", "인터럽트가 끼어듦", WARN)
node(3, 2, "잃어버린 갱신", "50 에서 51 로만", ACC)
harrow(3, 0, "세 명령 사이에")
harrow(3, 1, "같은 값을 읽어")

node(4, 0, "임계 구역", "공유 변수를 만짐", INFO)
node(4, 1, "상호 배제", "한 번에 한 스레드", INFO)
node(4, 2, "원자성", "전부 아니면 전무", OK)
harrow(4, 0, "여기만 지키면")
harrow(4, 1, "이 구간은")

node(5, 0, "하드웨어 지원", "특별한 명령", INFO)
node(5, 1, "동기화 기본 요소", "락 같은 도구", ACC)
node(5, 2, "조건 변수", "다른 스레드를 기다림", OK)
harrow(5, 0, "운영체제와 함께")
harrow(5, 1, "기다림은")

d.legend(H - 40, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 문제", ACC)])
d.save("20-01.chapter-overview.svg")
print("ok 20-01 overview")
