# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 지구를 경도·위도 비트 한 쌍씩 두 번 나눈 2×2 와 4×4 칸에 실제 비트 코드를 달아 접두사 01 이 가리키는 칸을 보인다.
# 사실 출처: 추출본 v1.txt 3583~3597행(위도 [-90,0]=0·[0,90]=1, 경도 [-180,0]=0·[0,180]=1, 경도 비트와 위도 비트를 번갈아 코드 구성, `LIKE '01%'`)과 PDF 145쪽 그림(2×2: 01 11 / 00 10, 4×4: 0101 0111 1101 1111 / 0100 0110 1100 1110 / 0001 0011 1001 1011 / 0000 0010 1000 1010).
#   칸 코드는 이 생성기가 경도 비트 b1 b2 · 위도 비트 a1 a2 로 b1 a1 b2 a2 를 계산해 달았고 그림의 16 코드와 일치한다.
# Layout conventions: 2×2 칸 104×112, 4×4 칸 128×56 로 두 격자 높이를 224 로 맞춤, 열 stride=칸 폭·행 stride=칸 높이, 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 512
d = D(W, H, "BYTEBYTEGO · 09-01 §3",
      "비트 한 쌍이 한 번 나눌 때마다 붙고 접두사가 칸을 가리킨다",
      "경도 비트와 위도 비트를 번갈아 붙인 코드의 앞 두 비트 01 이 북서 한 칸이고 그 안에 네 칸이 모두 들어 있습니다.",
      "경도 0 은 서쪽 절반·1 은 동쪽 절반, 위도 0 은 남쪽 절반·1 은 북쪽 절반입니다")

Y0 = 156
# 왼쪽: 한 번 나눈 2×2.
LX, LCW, LCH = 60, 104, 112
d.t(12, 132, "한 번 나눔 · 비트 한 쌍", 13, INK, KR, "start", 600)
for c, lab in enumerate(["경도 0", "경도 1"]):
    d.t(LX + c * LCW + LCW / 2, Y0 - 8, lab, 12, MUTED, KR, "middle")
for r, lab in enumerate(["위도 1", "위도 0"]):
    d.t(LX - 8, Y0 + r * LCH + LCH / 2 + 5, lab, 12, MUTED, KR, "end")
for r, lat in enumerate("10"):
    for c, lon in enumerate("01"):
        code = lon + lat
        x, y = LX + c * LCW, Y0 + r * LCH
        if code == "01":
            d.tone(x, y, LCW, LCH, ACC, 0, "14", 1.4)
            d.t(x + LCW / 2, y + LCH / 2 + 5, code, 16, ACC, MONO, "middle", 600)
        else:
            d.box(x, y, LCW, LCH, PAPER2, RULE, 0.9, 0)
            d.t(x + LCW / 2, y + LCH / 2 + 5, code, 16, INK, MONO, "middle", 600)

d.arrow([(LX + 2 * LCW + 12, Y0 + 112), (LX + 2 * LCW + 56, Y0 + 112)], MUTED, "ar", 1.4)

# 오른쪽: 한 번 더 나눈 4×4.
RX, RCW, RCH = 372, 128, 56
d.t(RX, 132, "한 번 더 나눔 · 비트 한 쌍 추가", 13, INK, KR, "start", 600)
col_bits = ["00", "01", "10", "11"]
row_bits = ["11", "10", "01", "00"]
for c, b in enumerate(col_bits):
    d.t(RX + c * RCW + RCW / 2, Y0 - 8, "경도 " + b, 12, MUTED, KR, "middle")
for r, a in enumerate(row_bits):
    d.t(RX - 8, Y0 + r * RCH + RCH / 2 + 5, "위도 " + a, 12, MUTED, KR, "end")
for r, a in enumerate(row_bits):
    for c, b in enumerate(col_bits):
        code = b[0] + a[0] + b[1] + a[1]
        x, y = RX + c * RCW, Y0 + r * RCH
        if code.startswith("01"):
            d.tone(x, y, RCW, RCH, ACC, 0, "14", 1.4)
            d.t(x + RCW / 2, y + RCH / 2 + 5, code, 16, ACC, MONO, "middle", 600)
        else:
            d.box(x, y, RCW, RCH, PAPER2, RULE, 0.9, 0)
            d.t(x + RCW / 2, y + RCH / 2 + 5, code, 16, INK, MONO, "middle", 600)

d.chip(RX + 2 * RCW, Y0 + 4 * RCH + 36, "geohash LIKE '01%'", ACC, 12)
d.legend(H - 48, [("접두사 01 이 가리키는 칸", ACC), ("나머지 칸", MUTED)])
d.save("09-01.geohash-grid.svg")
