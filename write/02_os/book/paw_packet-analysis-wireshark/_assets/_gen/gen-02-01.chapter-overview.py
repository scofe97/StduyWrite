# 타입 스펙: type-architecture — 키워드 개념도. 인터페이스 → 옵션 → 캡처 필터 → 파일 → 분할, 서버 캡처와 안 보일 때의 확인으로 이어지는 3행 × 3열 노드 격자.
# 사실 출처: 02-01 핵심 요약·학습 목표·키워드 표, §1 ~ §7 의 `>` 요약, §5 `-b duration:60 -b files:10` 예, §6 `tcpdump -w`, §7 목록 유무 가르기
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, OK, KR, MONO

COL_X, STRIDE, NW, NH = 64, 312, 208, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 920, 536


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 02-01 OVERVIEW",
      "캡처 필터가 버린 패킷은 어떤 필터로도 되살릴 수 없습니다",
      "02-01 의 키워드 개념도. 윗줄은 인터페이스 목록에서 이름으로 인터페이스를 고르고 Capture Options 로 받을 프레임을 정하는 흐름이다. "
      "가운데 줄은 캡처 필터가 커널에서 통과한 프레임만 파일로 보내고, 오래 잡을 때는 duration 과 files 조건으로 파일을 나누는 흐름이다. "
      "아랫줄은 Wireshark 가 없는 서버에서 tcpdump -w 로 파일을 뜨는 길과, 안 보일 때 인터페이스 목록 유무로 권한과 모드를 가르는 길이다.",
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


for i, sec in enumerate(("§1~3", "§4~5", "§6~7")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "인터페이스 목록", "네 입구 · 한 화면")
node(0, 1, "en0 · lo0 · eth0", "이름 = 매체 종류")
node(0, 2, "Capture Options", "promiscuous · snaplen")
harrow(0, 0, "이름이 가리킴")
harrow(0, 1, "골라서 설정")
wrap(0, "디스크 앞에서 거름")

node(1, 0, "캡처 필터", "BPF · 버린 건 복구 불가", ACC)
node(1, 1, "캡처 파일", "통과한 프레임만 저장", OK)
node(1, 2, "파일 분할", "duration:60 · files:10")
harrow(1, 0, "통과한 것만")
harrow(1, 1, "오래 잡으면")
wrap(1, "GUI 없는 곳은")

node(2, 0, "tcpdump -w", "서버에서 떠서 파일로")
node(2, 1, "인터페이스 목록", "뜨는지로 먼저 가름")
node(2, 2, "권한 · promiscuous", "비면 권한 · 있으면 모드")
harrow(2, 0, "안 잡히면")
harrow(2, 1, "유무로 갈림")

d.legend(472, [("핵심 접점", ACC), ("디스크에 남는 것", OK)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01 overview")
