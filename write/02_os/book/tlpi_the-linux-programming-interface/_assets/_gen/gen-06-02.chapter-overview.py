# 06-02 개념도 — 변수의 선언이 세그먼트를 정하고, 페이지 테이블이 가상 주소를 물리 프레임에 잇고, 함수 호출이 스택 프레임을 쌓고, longjmp 가 그 프레임을 되감는다.
# 본문 요구(06-02 「학습 목표」 개념도 문단): 1행 변수 선언·다섯 세그먼트·BSS(§1), 2행 가상 페이지·페이지 테이블·물리 프레임(§2),
#           3행 함수 호출·스택 프레임·반환(§3), 4행 setjmp·longjmp·중간 프레임 파기(§4), 5행 최적화 컴파일러·옛 값 복원·volatile(§4).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: TLPI 6.3·6.4·6.5·6.8, setjmp(3) CAVEATS.
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(04-01 개념도와 같은 공식: 열 x = 60 + j·340, 노드 216×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 104
W, H = 984, 672


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 06-02 OVERVIEW",
      "프로세스 메모리는 세그먼트로 나뉘고 페이지로 번역된다",
      "06-02 의 키워드 개념도. 1행은 변수의 선언 위치와 초기화 여부가 다섯 세그먼트 중 자리를 정하고 BSS 는 크기만 파일에 남기는 흐름이다. "
      "2행은 가상 페이지가 프로세스마다 하나인 페이지 테이블을 거쳐 물리 프레임에 이어지는 흐름이다. "
      "3행은 함수 호출마다 스택 프레임이 쌓이고 반환하면 제거되는 흐름이다. "
      "4행은 setjmp 가 저장한 스택 포인터와 프로그램 카운터로 longjmp 가 중간 프레임을 파기하는 흐름이다. "
      "5행은 최적화 컴파일러가 점프를 모르고 레지스터 변수를 옛 값으로 되돌리며 volatile 로 막는 흐름이다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "변수 선언", "위치와 초기화 여부", INFO)
node(0, 1, "다섯 세그먼트", "텍스트·데이터·BSS·힙·스택", INFO)
node(0, 2, "BSS 는 크기만", "파일에 바이트 없음", OK)
harrow(0, 0, "자리를 정해")
harrow(0, 1, "0 으로 채우니")

node(1, 0, "가상 페이지", "고정 크기 블록", INFO)
node(1, 1, "페이지 테이블", "프로세스마다 하나", ACC)
node(1, 2, "물리 프레임", "격리·공유·보호", OK)
harrow(1, 0, "엔트리로 찾아")
harrow(1, 1, "가리키는 곳")

node(2, 0, "함수 호출", "중첩해서 부름", INFO)
node(2, 1, "스택 프레임", "변수·호출 연결 정보", INFO)
node(2, 2, "반환", "프레임을 하나씩 제거", OK)
harrow(2, 0, "호출마다 쌓아")
harrow(2, 1, "끝나면 내려")

node(3, 0, "setjmp", "SP·PC 를 env 에 저장", INFO)
node(3, 1, "longjmp", "저장한 SP·PC 로 복원", INFO)
node(3, 2, "중간 프레임 파기", "setjmp 자리에서 재개", OK)
harrow(3, 0, "env 를 넘겨")
harrow(3, 1, "스택을 되감아")

node(4, 0, "최적화 컴파일러", "변수를 레지스터에", WARN)
node(4, 1, "옛 값으로 복원", "setjmp 시점의 값", WARN)
node(4, 2, "volatile", "매번 메모리에서 읽기", OK)
harrow(4, 0, "점프를 몰라")
harrow(4, 1, "막으려면")

d.legend(H - 40, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 개념", ACC)])
d.save("06-02.chapter-overview.svg")
print("ok 06-02 overview")
