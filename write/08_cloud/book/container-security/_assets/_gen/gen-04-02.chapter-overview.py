# 타입 스펙: type-architecture — 키워드 개념도. network namespace 의 lo 와 veth 쌍, user namespace 의 uid_map, IPC·cgroup namespace, 호스트에서 본 PID 와 전용 호스트의 네 줄을 잇는 4행 × 3열 노드 격자. focal 은 user namespace.
# 사실 출처: 노트 L21~L23(핵심 요약), L47~L60(lo 하나·veth 쌍), L83~L105(user namespace·uid_map), L135~L147(IPC·cgroup namespace), L174~L184(PID 10 · 30591), L194~L198(전용 호스트·Thin OS·불변).
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


d = D(W, H, "ARCHITECTURE · 04-02 OVERVIEW",
      "user namespace 가 컨테이너 안의 root 를 호스트의 비특권 사용자로 바꿉니다",
      "04-02 의 키워드 개념도. 첫 줄은 network namespace 가 lo 하나로 시작해 veth 쌍으로 바깥과 이어지는 흐름이다. "
      "둘째 줄은 user namespace 가 uid_map 의 0 1000 1 로 컨테이너 root 를 호스트의 비특권 사용자에 대응시켜 rootless 컨테이너를 가능하게 하는 흐름이다. "
      "셋째 줄은 IPC namespace 를 ipcs 로 확인하고 커널 4.6 에서 추가된 cgroup namespace 로 이어지는 흐름이다. "
      "넷째 줄은 컨테이너 안 PID 10 이 호스트에서 PID 30591 로 보이고, 그래서 컨테이너 전용 호스트를 권하는 흐름이다.",
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
    fit(label, 12, x2 - x1 - 8)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4~5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "network namespace", "인터페이스·라우팅 격리", INFO)
node(0, 1, "lo 하나", "그마저 DOWN", BAD)
node(0, 2, "veth 쌍", "ve1 · ve2", OK)
harrow(0, 0, "시작 상태")
harrow(0, 1, "케이블 연결")
wrap(0, "ID 시야로 넘어감")

node(1, 0, "user namespace", "컨테이너 root → 비특권", ACC)
node(1, 1, "uid_map", "0 1000 1")
node(1, 2, "rootless 컨테이너", "탈출해도 비특권", OK)
harrow(1, 0, "매핑 파일")
harrow(1, 1, "결과")
wrap(1, "나머지 두 namespace")

node(2, 0, "IPC namespace", "공유 메모리·메시지 큐", INFO)
node(2, 1, "ipcs", "자기 IPC 객체만 보임")
node(2, 2, "cgroup namespace", "커널 4.6 부터", INFO)
harrow(2, 0, "확인")
harrow(2, 1, "다음 namespace")
wrap(2, "시선을 호스트로")

node(3, 0, "PID 10 = 30591", "안과 밖의 번호", INFO)
node(3, 1, "VM 과 다른 가시성", "호스트 접근 = 전체 노출", BAD)
node(3, 2, "전용 호스트", "Thin OS · 불변 운영", OK)
harrow(3, 0, "호스트에서 보임")
harrow(3, 1, "그래서")

d.legend(600, [("격리 조각", INFO), ("한계·위험", BAD), ("핵심 접점", ACC), ("해결", OK)])
d.save(str(ASSETS / "04-02.chapter-overview.svg"))
print("ok 04-02 overview")
