# 타입 스펙: type-architecture — 키워드 개념도. 공격 → cgroup → 파일시스템, 파일 조작 세 동작, 런타임 감싸기와 v2 로 이어지는 3행 × 3열 노드 격자.
# 사실 출처: 노트 L21~L23(핵심 요약), L47(pid), L63(/sys/fs/cgroup), L77~L79(mkdir), L140~L148(limit·procs), L170~L173(docker --memory), L189·L215(v2)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 536


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 03-01 OVERVIEW",
      "cgroup 은 디렉토리를 만들고 파일에 값을 쓰는 일로 다룹니다",
      "03-01 의 키워드 개념도. 윗줄은 자원 고갈 공격을 cgroup 이 막고 커널이 /sys/fs/cgroup 에 의사 파일시스템으로 노출하는 모습이다. "
      "가운데 줄은 mkdir 로 cgroup 을 만들고 memory.limit_in_bytes 에 한도를, cgroup.procs 에 PID 를 쓰는 세 동작이다. "
      "아랫줄은 docker run --memory 100M 이 같은 일을 감싸고 cgroup v2 가 계층을 하나로 합치는 흐름이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    fit(title, 13, NW - 16)
    fit(sub, 12, NW - 16)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1~2", "§3~4", "§5~6")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "자원 고갈 공격", "굶기기 · fork bomb", BAD)
node(0, 1, "cgroup", "메모리 · CPU · pids 제한", INFO)
node(0, 2, "/sys/fs/cgroup", "의사 파일시스템", ACC)
harrow(0, 0, "막는 장치")
harrow(0, 1, "커널이 노출")
wrap(0, "파일 조작으로 다룸")

node(1, 0, "mkdir memory/liz", "cgroup 만들기")
node(1, 1, "memory.limit_in_bytes", "한도 · 초과 시 Killed")
node(1, 2, "cgroup.procs", "PID 배정")
harrow(1, 0, "숫자 쓰기")
harrow(1, 1, "PID 쓰기")
wrap(1, "런타임이 감쌈")

node(2, 0, "docker run --memory 100M", "limit_in_bytes 104857600")
node(2, 1, "docker/<컨테이너 ID>", "cgroup 이름 = 컨테이너 ID")
node(2, 2, "cgroup v2", "프로세스 하나 · 그룹 하나", OK)
harrow(2, 0, "만든 cgroup")
harrow(2, 1, "구조 변경")

d.legend(472, [("공격", BAD), ("핵심 접점", ACC), ("cgroup", INFO), ("v2", OK)])
d.save(str(ASSETS / "03-01.chapter-overview.svg"))
print("ok 03-01 overview")
