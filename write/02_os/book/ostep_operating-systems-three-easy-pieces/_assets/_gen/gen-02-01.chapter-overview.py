# 02-01 개념도 — 물리 CPU 가 몇 개뿐이어도 프로세스라는 추상과 시분할로 CPU 가 끝없이 있는 듯 보이게 만들고, 프로세스는 상태와 PCB 로 추적된다.
# 본문 요구(02-01 「학습 목표」 개념도 문단): 1행 시분할과 가상 CPU(§1), 2행 프로세스 API(§2), 3행 프로그램의 적재와 main 진입(§3),
#           4행 Ready·Running·Blocked 전이(§4), 5행 프로세스 목록·PCB·zombie(§5), 6행 process-run.py 숙제(§6).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 4장 §4.1~§4.6 과 Homework (Simulation).
# 타입 스펙: type-architecture — 키워드 개념도. 6행 × 3열 노드 격자(04-01 개념도와 같은 공식: 열 x = 60 + j·340, 노드 216×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 104
W, H = 984, 776


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 02-01 OVERVIEW",
      "프로세스는 CPU 를 번갈아 쓰며 끝없는 CPU 의 환상을 만든다",
      "02-01 의 키워드 개념도. 1행은 물리 CPU 가 몇 개뿐이어도 프로세스를 번갈아 돌려 가상 CPU 가 여럿인 듯 보이게 하는 시분할이다. "
      "2행은 프로세스를 만들고 기다리고 제어하고 없애고 살피는 API 다. 3행은 디스크의 프로그램이 주소 공간에 올라 main 에서 시작하는 과정이다. "
      "4행은 Ready 와 Running 과 Blocked 사이의 전이이고, 5행은 프로세스 목록과 PCB 와 zombie 상태다. 6행은 process-run.py 시뮬레이터 숙제다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5", "§6")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "물리 CPU 몇 개", "프로그램은 수십~수백", INFO)
node(0, 1, "시분할", "돌리다 멈추고 다음 실행", INFO)
node(0, 2, "가상 CPU 여럿", "끝없이 있는 듯한 환상", ACC)
harrow(0, 0, "번갈아 돌려")
harrow(0, 1, "겉으로는")

node(1, 0, "생성", "셸 명령 · 아이콘 클릭", INFO)
node(1, 1, "대기 · 제어", "wait · 멈춤과 재개", INFO)
node(1, 2, "소멸 · 상태", "강제 종료 · 실행 시간", OK)
harrow(1, 0, "만든 뒤")
harrow(1, 1, "끝내거나 살피려")

node(2, 0, "디스크의 프로그램", "code · static data", INFO)
node(2, 1, "주소 공간", "코드 · 힙 · 스택", INFO)
node(2, 2, "main() 진입", "CPU 제어를 넘김", OK)
harrow(2, 0, "읽어서 올려")
harrow(2, 1, "초기화한 뒤")

node(3, 0, "Ready", "돌 준비는 됨", INFO)
node(3, 1, "Running", "CPU 에서 실행 중", ACC)
node(3, 2, "Blocked", "I/O 완료를 기다림", WARN)
harrow(3, 0, "scheduled")
harrow(3, 1, "I/O: initiate")

node(4, 0, "프로세스 목록", "모든 프로세스를 추적", INFO)
node(4, 1, "PCB", "struct proc", ACC)
node(4, 2, "zombie", "끝났지만 정리 전", WARN)
harrow(4, 0, "항목마다")
harrow(4, 1, "끝나면")

node(5, 0, "process-run.py", "상태 변화 시뮬레이터", INFO)
node(5, 1, "-c · -p 플래그", "예측과 대조", INFO)
node(5, 2, "CPU 이용률", "I/O 때 전환하는지", OK)
harrow(5, 0, "예측한 뒤")
harrow(5, 1, "견주어")

d.legend(H - 40, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 대상", ACC)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01 overview")
