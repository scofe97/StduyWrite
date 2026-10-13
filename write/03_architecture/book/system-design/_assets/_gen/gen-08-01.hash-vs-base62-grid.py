# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 키 길이 · ID 생성기 · 충돌 · 다음 키, 열은 해시 + 충돌 해소와 base62 변환이고 칸 색이 강점(ok) · 조건부(warn) · 약점(bad)을 가른다.
# 사실 출처: 추출본 v2.txt 2232~2237행·PDF 127쪽 Table 8-3(길이 고정/증가·ID 생성기 불필요/필요·충돌 가능/불가·다음 URL 예측 불가/가능),
#   값은 직접 계산: CRC32(https://en.wikipedia.org/wiki/Systems_design) = 5cb54054 (본문 §4 표의 값, 격자에는 쓰지 않음), base62(11157) = 2TX, base62(11158) = 2TY, base62(2009215674938) = zn9edcu.
# Layout conventions: 행 이름 열 x=24 폭 168, 열 둘 폭 360 · 간격 8(x=208 · 576), 머리 y=96 높이 40, 줄 y=148 부터 stride 84 높이 76. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 584
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 08-01 §5",
      "해시는 키 길이를 고정하고 base62 는 충돌을 없앤다",
      "해시 + 충돌 해소는 길이가 7 자로 고정되고 ID 가 필요 없는 대신 충돌을 풀어야 하며, base62 는 충돌이 없는 대신 ID 생성기와 예측 가능한 키를 받는다.",
      "칸 색은 강점 · 조건부 · 약점")

X0, CW, STRIDE = 208, 360, 368
HY, RY, RS, RH = 96, 148, 84, 76
COLS = ("해시 + 충돌 해소", "base62 변환")
ROWS = (
    ("키 길이", (("7 자 고정", "62 진수 끝 7 자", OK, False), ("ID 가 커지면 늘어남", "2TX → zn9edcu", WARN, False))),
    ("ID 생성기", (("필요 없음", "URL 만 있으면 됨", OK, False), ("필요함", "유일 ID 를 받아 변환", WARN, True))),
    ("충돌", (("생길 수 있음", "재해시 · 블룸 필터", WARN, False), ("없음", "ID 가 유일", OK, False))),
    ("다음 키", (("알 수 없음", "ID 와 무관", OK, False), ("추측 가능", "11157 → 2TX · 11158 → 2TY", BAD, False))),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, name in enumerate(COLS):
    x = X0 + STRIDE * i
    d.box(x, HY, CW, 40, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 26, name, 14, INK, KR, "middle", 600)

for r, (name, cells) in enumerate(ROWS):
    y = RY + RS * r
    d.t(24, y + 44, name, 14, INK, KR, "start", 600)
    for i, (a, b, c, focal) in enumerate(cells):
        x = X0 + STRIDE * i
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            col = ACC
        else:
            d.tone(x, y, CW, RH, c, 6, "12", 1.2)
            col = c
        d.t(x + CW / 2, y + 32, a, 15, col, fam(a), "middle", 600)
        d.t(x + CW / 2, y + 56, b, 13, MUTED, fam(b))

d.legend(H - 56, [("강점", OK), ("조건부", WARN), ("약점", BAD), ("대가로 치르는 값", ACC)])
d.save("08-01.hash-vs-base62-grid.svg")
