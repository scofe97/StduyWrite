# 타입 스펙: type-architecture — 키워드 개념도. 네 개 창 → 컬러링 규칙 → 디스플레이 필터, 필드 선택 → 목록 → 계층, 사실과 판단과 추측으로 이어지는 3행 × 3열 노드 격자.
# 사실 출처: 02-02 핵심 요약·학습 목표·키워드 표, §1 ~ §6 의 `>` 요약, §3 `ip.addr`·`ip.src` 비교, §4 일곱 열·시간 기준, §5 Frame 메타 계층, §6 대괄호 판단
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, BAD, INFO, KR, MONO

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


d = D(W, H, "ARCHITECTURE · 02-02 OVERVIEW",
      "디스플레이 필터는 지우지 않고 시야만 좁힙니다",
      "02-02 의 키워드 개념도. 윗줄은 네 개 창이 같은 바이트를 보여주고 컬러링 규칙이 이상한 줄을 먼저 띄우며 디스플레이 필터가 시야를 좁히는 흐름이다. "
      "가운데 줄은 ip.addr 로 대화를 고르면 Packet List 의 일곱 열과 Packet Details 의 계층으로 내려가는 흐름이다. "
      "아랫줄은 Frame 줄이 선 위의 프로토콜이 아니고, 대괄호 필드는 판단이며, 표시 없는 추측이 사실처럼 읽히는 점을 가르는 흐름이다.",
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


for i, sec in enumerate(("§1~3", "§3~5", "§5~6")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "네 개 창", "목록 · 계층 · 바이트")
node(0, 1, "컬러링 규칙", "이상한 줄이 먼저 보임")
node(0, 2, "디스플레이 필터", "파일은 그대로 · 시야만", ACC)
harrow(0, 0, "목록 줄에 칠함")
harrow(0, 1, "찾은 줄을 좁힘")
wrap(0, "필드를 고르면")

node(1, 0, "ip.addr", "양쪽 매칭 · 대화가 보임")
node(1, 1, "Packet List", "일곱 열 · Time 기준 변경")
node(1, 2, "Packet Details", "frame 부터 응용 계층")
harrow(1, 0, "남은 줄이")
harrow(1, 1, "고른 줄을 펼침")
wrap(1, "맨 윗줄이")

node(2, 0, "Frame 줄", "선 위 프로토콜이 아님")
node(2, 1, "[ ] 대괄호 필드", "여러 프레임을 대조한 판단", INFO)
node(2, 2, "표시 없는 추측", "관습으로 붙어 사실처럼", BAD)
harrow(2, 0, "얹은 값은")
harrow(2, 1, "표시 없으면")

d.legend(472, [("핵심 접점", ACC), ("표시된 판단", INFO), ("표시 없는 추측", BAD)])
d.save("02-02.chapter-overview.svg")
print("ok 02-02 overview")
