# 06-03 개념도 — 인자 목록과 환경 목록은 execve() 가 새 프로그램에 건네고, 환경 목록은 자식이 생성 때 사본으로 물려받으며, 프로그램은 putenv()·setenv() 로 그 목록을 고친다.
# 본문 요구(06-03 「학습 목표」 개념도 문단): 1행 명령 줄·argc·argv·NULL 종단(§1), 2행 인자·환경 문자열 영역·ARG_MAX·E2BIG(§2),
#           3행 부모 환경·자식의 사본·단방향 일회성(§3), 4행 environ·putenv()·setenv()(§4).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: TLPI 6.6~6.7, execve(2) 「Limits on size of arguments and environment」, putenv(3)·setenv(3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(열 x = 56 + j·300, 노드 200×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 56, 300, 200, 64
ROW_Y, ROW_STRIDE = 112, 104
W, H = 880, 560


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "TLPI · 06-03",
      "인자와 환경은 execve() 가 건네고 자식은 환경의 사본을 받는다",
      "06-03 의 키워드 개념도. 1행은 셸이 쪼갠 명령 줄이 argc 와 argv 로 main() 에 건네지고 argv 가 NULL 로 끝난다는 흐름이다. "
      "2행은 인자와 환경 문자열이 스택 위 한 영역에 놓이고 ARG_MAX 한도를 넘으면 execve() 가 E2BIG 로 실패한다는 흐름이다. "
      "3행은 부모의 환경 목록이 자식 생성 때 한 번 복사되고 이후 수정이 서로 보이지 않는다는 흐름이다. "
      "4행은 environ 을 고치는 putenv() 가 포인터를 그대로 등록해 위험하고 setenv() 는 문자열을 복사해 안전하다는 흐름이다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(28, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "명령 줄", "셸이 단어로 쪼갬", INFO)
node(0, 1, "argc · argv", "개수와 포인터 배열", ACC)
node(0, 2, "argv[argc]", "항상 NULL", OK)
harrow(0, 0, "건네는 값")
harrow(0, 1, "배열의 끝")

node(1, 0, "인자 · 환경", "스택 위 한 영역", INFO)
node(1, 1, "ARG_MAX", "RLIMIT_STACK 의 1/4", INFO)
node(1, 2, "E2BIG", "한도를 넘으면 실패", WARN)
harrow(1, 0, "크기 상한")
harrow(1, 1, "넘으면")

node(2, 0, "부모 환경", "NAME=value 목록", INFO)
node(2, 1, "자식의 사본", "생성 때 한 번 복사", ACC)
node(2, 2, "단방향 일회성", "이후 수정은 안 보임", OK)
harrow(2, 0, "물려줌")
harrow(2, 1, "그 뒤로")

node(3, 0, "environ", "NULL 로 끝나는 배열", INFO)
node(3, 1, "putenv()", "포인터를 그대로 등록", WARN)
node(3, 2, "setenv()", "문자열을 복사해 등록", OK)
harrow(3, 0, "고치는 길")
harrow(3, 1, "안전한 쪽")

d.legend(H - 56, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 개념", ACC)])
d.save("06-03.chapter-overview.svg")
print("ok 06-03 overview")
