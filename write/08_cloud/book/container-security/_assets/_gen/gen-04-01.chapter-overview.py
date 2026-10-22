# 타입 스펙: type-architecture — 키워드 개념도. namespace 개관·UTS, PID 두 번의 실패, 루트 변경과 proc 마운트, mount namespace 의 네 줄을 잇는 4행 × 3열 노드 격자. focal 은 ps 가 읽는 /proc.
# 사실 출처: 노트 L21~L23(핵심 요약), L43~L65(namespace 종류), L95~L104(unshare --uts sh), L120~L146(--pid · --fork · /proc), L174~L206(chroot alpine · mount -t proc), L222~L242(--mount · bind).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 664


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-01 OVERVIEW",
      "ps 를 격리하려면 PID namespace 에 새 루트와 proc 마운트를 겹쳐야 합니다",
      "04-01 의 키워드 개념도. 첫 줄은 namespace 종류 중 UTS 를 unshare --uts sh 로 만들어 호스트명을 바꾸는 흐름이다. "
      "둘째 줄은 unshare --pid 의 Cannot fork 와 --fork 뒤에도 호스트 프로세스가 보이는 ps 가 /proc 으로 이어지는 흐름이다. "
      "셋째 줄은 chroot alpine 으로 루트를 바꾼 뒤 mount -t proc proc /proc 를 하면 ps 가 자기 프로세스만 보여 주는 흐름이다. "
      "넷째 줄은 같은 구조가 mount namespace 의 bind 마운트에도 되풀이되는 흐름이다.",
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


for i, sec in enumerate(("§1~2", "§3", "§4~5", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "namespace 일곱 종류", "볼 수 있는 것을 통제", INFO)
node(0, 1, "UTS namespace", "unshare --uts sh")
node(0, 2, "호스트명 격리", "hostname experiment", OK)
harrow(0, 0, "종류 하나")
harrow(0, 1, "이름 변경")
wrap(0, "프로세스 격리로 넘어감")

node(1, 0, "unshare --pid", "Cannot fork", BAD)
node(1, 1, "unshare --pid --fork", "ps 가 호스트 전체 출력", WARN)
node(1, 2, "/proc", "ps 가 읽는 가상 파일", ACC)
harrow(1, 0, "--fork 추가")
harrow(1, 1, "원인 추적")
wrap(1, "루트를 바꿔 /proc 교체")

node(2, 0, "chroot alpine", "새 루트 · pivot_root 가 안전")
node(2, 1, "mount -t proc proc /proc", "새 루트의 /proc 채움")
node(2, 2, "ps", "자기 PID namespace 만", OK)
harrow(2, 0, "루트 변경 후")
harrow(2, 1, "결과")
wrap(2, "mount 도 같은 구조")

node(3, 0, "unshare --mount sh", "mount namespace", INFO)
node(3, 1, "mount --bind", "source 를 target 에")
node(3, 2, "호스트에 안 보임", "docker run -v 도 같은 원리", OK)
harrow(3, 0, "bind 마운트")
harrow(3, 1, "결과")

d.legend(600, [("실패", BAD), ("누수", WARN), ("핵심 접점", ACC), ("격리 성공", OK), ("namespace", INFO)])
d.save(str(ASSETS / "04-01.chapter-overview.svg"))
print("ok 04-01 overview")
