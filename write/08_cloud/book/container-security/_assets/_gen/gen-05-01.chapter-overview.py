# 타입 스펙: type-architecture — 키워드 개념도. 부팅과 권한 링, VMM 의 세 배치, 트랩앤에뮬레이트와 가상화 불가 명령, 격리 강도로 모이는 3행 × 4열 노드 격자. focal 은 격리 강도.
# 사실 출처: 노트 L47~L65(BIOS·부트로더·커널·Ring), L73~L81(VMM), L95~L117(Type 1·Type 2·KVM), L123~L137(트랩·민감 명령·세 기법), L157~L171(Linux 2천만 줄·Xen 5만 줄)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 236, 180, 76
ROW_Y, ROW_STRIDE = 112, 128
W, H = 988, 528


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 05-01 OVERVIEW",
      "부팅에서 시작해 VMM 의 세 배치와 트랩앤에뮬레이트를 거쳐 격리 강도로 모입니다",
      "05-01 의 키워드 개념도. 윗줄은 BIOS 와 부트로더가 커널을 올리고 커널이 Ring 0 에서 프로세스를 관리하는 모습이다. "
      "가운데 줄은 BIOS 자리에 VMM 이 들어서고 Type 1, Type 2, KVM 세 배치로 갈리는 모습이다. "
      "아랫줄은 트랩앤에뮬레이트가 가상화 불가 명령에 막혀 세 기법을 쓰고, 마지막으로 Linux 와 Xen 의 코드 규모로 격리 강도를 비교하는 모습이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, subs, c=None):
    x, y = nx(j), ny(i)
    fit(title, 13, NW - 16)
    for s in subs:
        fit(s, 12, NW - 16)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 26, title, 13, c or INK, kr(title), "middle", 600)
    for n, s in enumerate(subs):
        d.t(x + NW / 2, y + 46 + n * 18, s, 12, MUTED, kr(s), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(3) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 28
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2~3", "§4~5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "BIOS · UEFI", ["하드웨어 열거"])
node(0, 1, "부트로더", ["커널 코드 적재"])
node(0, 2, "커널 · Ring 0", ["메모리 관리"])
node(0, 3, "프로세스 · Ring 3", ["서로의 메모리 접근 불가"])
harrow(0, 0, "다음")
harrow(0, 1, "다음")
harrow(0, 2, "관리")
wrap(0, "BIOS 자리에 VMM")

node(1, 0, "VMM", ["게스트 커널 하나씩"])
node(1, 1, "Type 1", ["Hyper-V · Xen · ESXi"], INFO)
node(1, 2, "Type 2", ["VirtualBox · Parallels"], INFO)
node(1, 3, "KVM", ["Linux 커널 모듈"], INFO)
harrow(1, 0, "분류")
harrow(1, 1, "OS 위")
harrow(1, 2, "커널 안")
wrap(1, "공통 기법")

node(2, 0, "트랩앤에뮬레이트", ["특권 명령 가로채기"])
node(2, 1, "가상화 불가 명령", ["민감하지만 비특권"], WARN)
node(2, 2, "세 가지 기법", ["바이너리 변환 · 반가상화", "하드웨어 가상화 VT-x"])
node(2, 3, "격리 강도", ["Linux 2천만 줄 이상", "Xen 약 5만 줄"], ACC)
harrow(2, 0, "한계")
harrow(2, 1, "해법")
harrow(2, 2, "비교")

d.legend(484, [("VMM 배치", INFO), ("난점", WARN), ("결론", ACC)])
d.save(str(ASSETS / "05-01.chapter-overview.svg"))
print("ok 05-01 chapter-overview")
