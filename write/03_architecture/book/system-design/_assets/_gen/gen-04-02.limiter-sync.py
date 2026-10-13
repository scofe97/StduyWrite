# 타입 스펙: type-architecture — 같은 요청 6건을 두 구성(제한기마다 카운터 · Redis 공유 카운터)에 두 줄로 대응시킨다. focal 은 공유 Redis 카운터 6.
# 사실 출처: 추출본 v2.txt 1231~1249행(제한기가 여럿이면 동기화 필요 · 스티키 세션은 비권장 · Redis 같은 중앙 저장소).
#   한도 5 · 요청 6건 · 번갈아 보냄(1·3·5 / 2·4·6)은 설명용 설계 값. 카운터 3 + 3 = 6 은 계산.
# Layout conventions: 존 폭 928·높이 216, 줄 stride 232(y=100·332), 노드 높이 56, 제한기 둘 stride 80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, INK, PAPER2, RULE, INFO, KR, MONO


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


W, H = 960, 632
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-02 §5",
      "제한기마다 따로 세면 여섯 건이 한도 다섯을 넘는다",
      "한도 5 에 요청 6건을 두 제한기에 번갈아 보내면 따로 센 카운터는 3 과 3 이라 모두 통과하고 Redis 한곳에서 세면 6 이라 여섯째가 429 를 받는다.",
      "같은 클라이언트의 요청 6건")


def node(x, y, w, title, sub, c=None):
    if c:
        d.tone(x, y, w, 56, c, 6, "12", 1.4 if c == ACC else 1.0)
    else:
        d.box(x, y, w, 56, PAPER2, RULE, 1.0)
    d.t(x + w / 2, y + 24, title, 14, INK, fam(title), "middle", 600)
    d.t(x + w / 2, y + 44, sub, 12, MUTED, fam(sub))


def row(y0, label, sub1, sub2, right_title, right_sub, right_color, chip_txt, chip_color):
    d.box(16, y0, 928, 216, PAPER2, RULE, 0.9, 8)
    d.t(32, y0 + 28, label, 13, MUTED, KR, "start", 600)
    yc, y1, y2, yr = y0 + 112, y0 + 76, y0 + 156, y0 + 116
    node(40, y0 + 84, 152, "클라이언트", "한도 5 · 요청 6", None)
    node(312, y0 + 48, 176, "제한기 1", sub1, None)
    node(312, y0 + 128, 176, "제한기 2", sub2, None)
    node(664, y0 + 88, 200, right_title, right_sub, right_color)
    for yy in (y1, y2):
        d.arrow([(194, yc), (252, yc), (252, yy), (310, yy)], MUTED, "ar", 1.5)
        d.arrow([(490, yy), (580, yy), (580, yr), (662, yr)], MUTED, "ar", 1.5)
    d.chip(764, y0 + 188, chip_txt, chip_color, 12)


row(100, "제한기마다 따로 센다", "요청 1·3·5 · counter 3", "요청 2·4·6 · counter 3",
    "API 서버", "6건 모두 통과", BAD, "3 ≤ 5 · 3 ≤ 5", BAD)
row(332, "Redis 하나를 같이 센다", "요청 1·3·5 · INCR", "요청 2·4·6 · INCR",
    "Redis", "counter 6", ACC, "6 > 5 · 429", OK)

d.legend(H - 56, [("공유 카운터", ACC), ("한도를 넘겨 통과", BAD), ("정상 차단", OK)])
d.save("04-02.limiter-sync.svg")
