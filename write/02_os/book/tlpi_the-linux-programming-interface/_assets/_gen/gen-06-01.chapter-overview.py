# 06-01 개념도 — 프로그램 파일에 커널이 자원을 붙이면 프로세스가 되고, PID 가 그 프로세스를 식별하며, PID 순환과 부모 사슬이 번호와 계보를 정한다.
# 본문 요구(06-01 「학습 목표」 개념도 문단): 1행 프로그램 파일·프로세스·프로세스 여럿(§1), 2행 프로세스·PID·kill·waitpid(§2),
#           3행 PID 카운터·300 으로 복귀·pid_max(§3), 4행 PPID·init·고아 입양(§4).
# 값 근거: 개념도라 값은 없다. 기본값 32,768 은 proc_sys_kernel(5) 의 pid_max.
# 공식 근거: TLPI 6.1~6.2, proc_sys_kernel(5), getpid(2), PR_SET_CHILD_SUBREAPER(2const).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(열 x = 150 + j·290, 노드 200×68), 행 안은 가로 화살표.
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, INFO, KR, MONO

W, ROW0, STRIDE, NW, NH = 960, 104, 100, 200, 68
H = ROW0 + 4 * STRIDE + 8 + 52
d = D(W, H, "TLPI · 06-01 OVERVIEW",
      "프로그램 파일이 프로세스가 되고 PID 와 부모 사슬로 식별된다",
      "1행은 프로그램 파일에 커널이 자원을 붙여 프로세스가 되는 과정, 2행은 PID 로 프로세스를 지목하는 방식, "
      "3행은 PID 가 상한에 닿으면 300 으로 되돌아가는 순환, 4행은 부모 사슬이 init 에 닿고 부모가 죽으면 고아가 입양되는 흐름이다.")


def nx(j):
    return 150 + j * 290


def node(j, i, title, sub, kind=None, mono=False):
    x, y = nx(j), ROW0 + i * STRIDE
    if kind:
        d.tone(x, y, NW, NH, kind, 6, "18", 1.4 if kind == ACC else 1.2)
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + NW / 2, y + 29, title, 14, INK, MONO if mono else KR, "middle", 600)
    d.t(x + NW / 2, y + 51, sub, 12, MUTED, KR)


def link(j, i, label):
    y = ROW0 + i * STRIDE + NH / 2
    x1, x2 = nx(j) + NW + 6, nx(j + 1) - 6
    d.arrow([(x1, y), (x2, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 8, label, 13, MUTED, KR)


rows = [
    ("1절", "프로그램과", "프로세스",
     [("프로그램 파일", "디스크의 정적 명세", MUTED, False), ("프로세스", "메모리와 커널 자료구조", INFO, False),
      ("프로세스 여럿", "PID·자원이 각자 따로", INFO, False)],
     ["자원 부여", "여러 번 실행"]),
    ("2절", "고유 식별자", "PID",
     [("프로세스", "식별할 번호가 필요", None, False), ("PID", "양의 정수 · pid_t", INFO, True),
      ("kill · waitpid", "PID 로 대상을 지정", None, True)],
     ["번호 부여", "대상 지정"]),
    ("3절", "PID 순환과", "상한",
     [("PID 카운터", "새 프로세스마다 증가", None, False), ("300 으로 복귀", "1~299 는 건너뜀", INFO, False),
      ("pid_max", "기본 32,768", None, True)],
     ["상한 도달", "상한은 조정"]),
    ("4절", "부모와", "프로세스 트리",
     [("PPID", "생성한 부모의 PID", None, True), ("init (PID 1)", "모든 프로세스의 조상", INFO, True),
      ("고아 입양", "init 이나 subreaper", ACC, False)],
     ["거슬러 오름", "부모 종료 시"]),
]
for i, (tag, l1, l2, nodes, labels) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.t(24, y + 26, tag, 14, INK, KR, "start", 600)
    d.t(24, y + 46, l1, 12, MUTED, KR, "start")
    d.t(24, y + 62, l2, 12, MUTED, KR, "start")
    for j, (t, s, k, m) in enumerate(nodes):
        node(j, i, t, s, k, m)
    for j, lb in enumerate(labels):
        link(j, i, lb)

d.legend(H - 52, [("정적 명세", MUTED), ("커널이 붙이거나 정하는 것", INFO), ("부모가 먼저 죽을 때", ACC)])
d.save("06-01.chapter-overview.svg")
print("ok 06-01 chapter-overview")
