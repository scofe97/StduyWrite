# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 장면 셋(친구 300 명의 게시 · 팔로워 5,000,000 명의 게시 · 팔로우 300 곳 사용자의 피드 열기), 열은 밀기 · 당기기 · 혼합이고 칸 색이 감당(ok) · 조건부(warn) · 폭발(bad)을 가른다.
# 사실 출처: 구조(밀기·당기기·혼합과 장단점)는 추출본 v2.txt 3047~3074행. 300 · 5,000,000 · 유명인 2 는 비교용 설계 가정이며 계산: 쓰기 = 게시 1 건당 받는 피드 수, 읽기(당기기) = 팔로우 300, 읽기(혼합) = 피드 캐시 1 + 유명인 2 = 3.
# Layout conventions: 행 이름 열 x=24 폭 224, 열 셋 폭 216 · 간격 8(x=264 · 488 · 712), 머리 y=96 높이 40, 줄 y=148 부터 stride 84 높이 76. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 472
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 11-01 §3",
      "밀기는 쓰기가 늘고 당기기는 읽기가 는다",
      "친구 300 명의 게시는 밀어도 쓰기 300 번이지만 팔로워 5,000,000 명의 게시는 밀면 쓰기 5,000,000 번이고, 팔로우 300 곳의 피드는 당기면 읽기 300 번이며 섞으면 3 번이다.",
      "게시 1 건의 쓰기 횟수와 피드 1 번의 읽기 횟수")

X0, CW, STRIDE = 264, 216, 224
HY, RY, RS, RH = 96, 148, 84, 76
COLS = ("쓸 때 밀기", "읽을 때 당기기", "섞기")
# (행 이름 둘째 줄, 행 이름 첫째 줄, 칸 셋 = (큰 글자, 작은 글자, 색, focal))
ROWS = (
    ("게시 1 건", "친구 300 명", (
        ("쓰기 300 번", "친구마다 1 번", OK, False),
        ("쓰기 0 번", "게시물만 저장", OK, False),
        ("쓰기 300 번", "일반 사용자는 밀기", OK, False))),
    ("게시 1 건", "팔로워 5,000,000 명", (
        ("쓰기 5,000,000 번", "한 게시물이 몰림", BAD, True),
        ("쓰기 0 번", "게시물만 저장", OK, False),
        ("쓰기 0 번", "유명인은 당기기", OK, False))),
    ("피드 열기 1 번", "팔로우 300 곳 · 유명인 2", (
        ("읽기 1 번", "피드 캐시 하나", OK, False),
        ("읽기 300 번", "팔로우마다 조회 · 병합", BAD, False),
        ("읽기 3 번", "캐시 1 + 유명인 2", WARN, False))),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, name in enumerate(COLS):
    x = X0 + STRIDE * i
    d.box(x, HY, CW, 40, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 26, name, 14, INK, KR, "middle", 600)

for r, (l1, l2, cells) in enumerate(ROWS):
    y = RY + RS * r
    d.t(24, y + 32, l1, 14, INK, KR, "start", 600)
    d.t(24, y + 56, l2, 13, MUTED, KR, "start")
    for i, (a, b, c, focal) in enumerate(cells):
        x = X0 + STRIDE * i
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            col = ACC
        else:
            d.tone(x, y, CW, RH, c, 6, "12", 1.2)
            col = c
        d.t(x + CW / 2, y + 32, a, 15, col, KR, "middle", 600)
        d.t(x + CW / 2, y + 56, b, 13, MUTED, KR)

d.legend(H - 56, [("감당", OK), ("조건부", WARN), ("폭발", BAD), ("폭발 중 가장 큰 비용", ACC)])
d.save("11-01.fanout-grid.svg")
