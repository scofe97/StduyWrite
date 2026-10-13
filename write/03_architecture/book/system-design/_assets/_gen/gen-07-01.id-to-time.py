# 타입 스펙: type-process — 실제 ID 하나를 이진수 필드로 쪼개고, 41비트가 십진수 → epoch 더하기 → UTC 날짜로 바뀌는 네 단계를 같은 값으로 따라간다.
# 사실 출처: 추출본 v2.txt 2037~2046행(설명 글. 41비트 예시 이진수 · 297616116568 · + 1288834974657 = 1586451091225 · Apr 09 2020 16:51:31 UTC 는 PDF 쪽 115 그림에서 직접 읽음).
#   ID 십진수 1248292468186988544 = 297616116568 × 2^22 + 10 × 2^17 + 12 × 2^12 + 0 으로 계산, 밀리초 .225 는 1586451091225 ms 의 나머지.
# Layout conventions: ID 카드 x=24 폭 216, 이진 칸 x=280 부터(글자 11px · 칸 폭 = 글자 수 × 7 + 16), 2줄 카드 x=280·500·720 폭 196 y=232 높이 88. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, INK, SOFT, KR, MONO

W, H = 960, 408
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §6",
      "ID 의 위쪽 41비트가 만든 시각으로 돌아온다",
      "ID 1248292468186988544 를 이진수로 쪼개면 41비트가 297616116568 ms 이고, epoch 를 더하면 2020-04-09 16:51:31.225 UTC 다.",
      "아래쪽 22비트는 만든 곳과 순번")

ID = "1248292468186988544"
d.tone(24, 108, 216, 40, INK, 6, "10", 1.0)
d.t(132, 100, "ID", 12, SOFT, KR)
d.t(132, 134, ID, 14, INK, MONO, "middle", 600)
d.arrow([(244, 128), (276, 128)], MUTED, "ar", 1.5)

BITS = (
    ("부호", "0", SOFT, None),
    ("시각", "00100010101001011010011011000101101011000", ACC, None),
    ("센터", "01010", INFO, "= 10"),
    ("머신", "01100", INFO, "= 12"),
    ("순번", "000000000000", OK, "= 0"),
)
x = 280
centers = {}
for name, b, c, dec in BITS:
    w = max(len(b) * 7 + 16, 28)
    d.tone(x, 108, w, 40, c, 4, "14" if c == ACC else "10", 1.4 if c == ACC else 1.0)
    d.t(x + w / 2, 100, name, 12, c, KR, "middle", 600)
    d.t(x + w / 2, 133, b, 11, c, MONO)
    if dec:
        d.chip(x + w / 2, 184, dec, c, 12)
    centers[name] = (x, w)
    x += w + 8
tx, tw = centers["시각"]
CX = (280, 500, 720)
CARDS = (
    ("41비트 → 십진수", ("297616116568",)),
    ("+ 1288834974657", ("1586451091225",)),
    ("밀리초 → UTC", ("2020-04-09", "16:51:31.225")),
)
d.arrow([(CX[0] + 180, 152), (CX[0] + 180, 228)], ACC, "acc", 1.5)
for i, (tag, vals) in enumerate(CARDS):
    c = ACC if i == 2 else INFO
    d.tone(CX[i], 232, 196, 88, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(CX[i] + 14, 260, tag, 12, c, MONO if i < 2 else KR, "start", 600)
    for k, v in enumerate(vals):
        d.t(CX[i] + 14, 292 + 20 * k, v, 14, INK, MONO, "start", 600)
    if i < 2:
        d.arrow([(CX[i] + 198, 276), (CX[i + 1] - 6, 276)], MUTED, "ar", 1.5)
d.legend(H - 56, [("부호", SOFT), ("시각", ACC), ("만든 곳", INFO), ("순번", OK)])
d.save("07-01.id-to-time.svg")
