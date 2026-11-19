# 03-01 개념도 — fork 가 복제하고 wait 가 기다리고 exec 이 덮어쓰며, 둘 사이의 틈에서 리다이렉션이 만들어지고, 시그널과 사용자 개념이 제어를 맡는다.
# 본문 요구(03-01 「학습 목표」 개념도 문단): 1행 fork·반환값·자식(§1), 2행 wait·자식 종료·순서 고정(§2), 3행 자식·exec·다른 프로그램(§3), 4행 파일 번호 조정·exec·리다이렉션(§4), 5행 kill·사용자·슈퍼유저(§5).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 5장 §5.1~§5.4, 5.6.
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


d = D(W, H, "ARCHITECTURE · 03-01 OVERVIEW",
      "fork 는 복제하고 exec 은 덮어쓰며 그 사이에서 환경이 바뀐다",
      "03-01 의 키워드 개념도. 1행은 fork 가 부모를 복제해 자식을 만들고 반환값으로 부모와 자식을 가르는 흐름이다. "
      "2행은 부모가 wait 로 막혀 있다가 자식이 끝나면 돌아와 출력 순서가 고정되는 흐름이다. "
      "3행은 자식이 exec 으로 다른 프로그램이 되는 흐름이다. "
      "4행은 자식이 열린 파일을 바꾼 뒤 exec 을 불러 리다이렉션이 되는 흐름이다. "
      "5행은 kill 로 시그널을 보내고 사용자 개념이 보낼 수 있는 대상을 정하는 흐름이다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "fork()", "호출한 프로세스를 복제", INFO)
node(0, 1, "반환값", "부모는 PID · 자식은 0", ACC)
node(0, 2, "자식 프로세스", "fork 자리부터 실행", OK)
harrow(0, 0, "돌아올 때")
harrow(0, 1, "갈래가 나뉘어")

node(1, 0, "wait()", "부모를 막아 둠", INFO)
node(1, 1, "자식 종료", "막힘이 풀림", WARN)
node(1, 2, "출력 순서 고정", "자식이 먼저", OK)
harrow(1, 0, "끝날 때까지")
harrow(1, 1, "돌아오면")

node(2, 0, "자식 프로세스", "부모의 복사본", INFO)
node(2, 1, "exec()", "코드·정적 데이터 덮어씀", ACC)
node(2, 2, "다른 프로그램", "성공하면 돌아오지 않음", OK)
harrow(2, 0, "안에서 부르면")
harrow(2, 1, "프로세스는 그대로")

node(3, 0, "파일 번호 조정", "close · open", INFO)
node(3, 1, "exec()", "열린 파일은 남음", ACC)
node(3, 2, "리다이렉션", "프로그램은 그대로", OK)
harrow(3, 0, "exec 전에")
harrow(3, 1, "출력이 파일로")

node(4, 0, "kill()", "시그널을 보냄", INFO)
node(4, 1, "사용자", "자기 프로세스만", WARN)
node(4, 2, "슈퍼유저", "모든 프로세스", OK)
harrow(4, 0, "누구에게 보낼지")
harrow(4, 1, "일반 사용자와 달리")

d.legend(H - 40, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("제약 · 위험", WARN), ("핵심 장치", ACC)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01 overview")
