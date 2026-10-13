# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 다섯 방식, 열은 숫자만 · 64비트 · 시간순 · 조율 없이이고 칸 색이 맞음(ok) · 조건부(warn) · 아님(bad)을 가른다.
# 사실 출처: 추출본 v2.txt 1922~2022행(요구사항 1922~1943, 방식별 장단점 1952~2002, 스노플레이크 2003~2022), Flickr 티켓 서버 글(Tickets64 · 두 대 홀짝 · 순서가 조금 어긋남), RFC 9562 §5.4·§5.7, 스노플레이크 README(k-sorted).
# Layout conventions: 방식 이름 열 x=24 폭 200, 열 넷 폭 168 · 간격 8(x=240 부터 stride 176), 머리 y=96 높이 40, 줄 y=148 부터 stride 68 높이 60. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §4",
      "네 가지 조건을 모두 채우는 방식은 스노플레이크뿐이다",
      "다중 마스터는 서버 사이 시간순을, UUID 는 숫자와 64비트를, 티켓 서버는 조율 없는 생성을 놓친다.",
      "칸 색은 맞음 · 조건부 · 아님")

X0, CW, STRIDE = 240, 168, 176
HY, RY, RS, RH = 96, 148, 68, 60
COLS = ("숫자만", "64비트", "시간순", "조율 없이")
ROWS = (
    ("다중 마스터", (("맞음", "정수", OK), ("맞음", "", OK), ("서버 사이", "역전", BAD), ("k 를", "바꿔야 함", WARN))),
    ("UUIDv4", (("아님", "16진 문자열", BAD), ("아님", "128비트", BAD), ("아님", "무작위", BAD), ("맞음", "서버마다 생성", OK))),
    ("UUIDv7", (("아님", "16진 문자열", BAD), ("아님", "128비트", BAD), ("맞음", "밀리초 단위", OK), ("맞음", "서버마다 생성", OK))),
    ("티켓 서버", (("맞음", "", OK), ("맞음", "", OK), ("한 대일 때", "발급 순", WARN), ("아님", "한 대에 몰림", BAD))),
    ("스노플레이크", (("맞음", "", OK), ("맞음", "64비트", OK), ("맞음", "밀리초 단위", OK), ("맞음", "머신마다 생성", OK))),
)
for i, name in enumerate(COLS):
    x = X0 + STRIDE * i
    d.box(x, HY, CW, 40, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 26, name, 14, INK, KR, "middle", 600)
for r, (name, cells) in enumerate(ROWS):
    y = RY + RS * r
    foc = r == 4
    d.t(24, y + 36, name, 14, ACC if foc else INK, KR, "start", 600)
    for i, (a, b, c) in enumerate(cells):
        x = X0 + STRIDE * i
        d.tone(x, y, CW, RH, c, 6, "12", 1.2)
        if b:
            d.t(x + CW / 2, y + 26, a, 14, c, KR, "middle", 600)
            d.t(x + CW / 2, y + 48, b, 13, MUTED, KR)
        else:
            d.t(x + CW / 2, y + 36, a, 14, c, KR, "middle", 600)
fy = RY + RS * 4
d.box(X0 - 4, fy - 4, STRIDE * 4 - 4, RH + 8, "none", ACC, 1.4, 8)
d.legend(H - 56, [("맞음", OK), ("조건부", WARN), ("아님", BAD), ("고른 방식", ACC)])
d.save("07-01.comparison-grid.svg")
