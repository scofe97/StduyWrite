# 타입 스펙: type-process — 4+2 이레이저 코딩의 네 단계(나눔 · 패리티 · 손실 · 복원)를 같은 여섯 조각을 단계마다 다시 그려 보인다. 값은 d1~d4 = 3·1·4·1 이고 아래 막대가 저장 공간 1 GB 기준 1.5 GB 대 3 GB 를 길이로 비교한다.
# 사실 출처: 추출본 v1.txt 2140~2170행(4+2, "much simplified" 식 p1 = d1 + 2*d2 - d3 + 4*d4 · p2 = -d1 + 5*d2 + d3 - 3*d4, d3·d4 손실, 저장 오버헤드 50% 대 200%)
#   · 풀이는 계산이다: p1 = 3+2-4+4 = 5, p2 = -3+5+4-3 = 3. (p1-d1-2·d2) = -d3+4·d4 = 0, (p2+d1-5·d2) = d3-3·d4 = 1, 둘을 더하면 d4 = 1, d3 = 1+3 = 4. 1 GB 를 4 조각 × 0.25 GB + 패리티 2 × 0.25 GB = 1.5 GB.
#   · Backblaze "Backblaze Open-sources Reed-Solomon Erasure Coding Source Code"(4+2 예시, 어느 n 조각으로든 복원)와 "Backblaze Vaults"(17 데이터 + 3 패리티, 20 조각 중 17 조각이면 복원).
# Layout conventions: 열 stride 224(x=24+224k, 폭 188), 조각 상자 폭 156·높이 32, 행 stride 40(y=128 부터 6행), 식 줄 stride 20, 비교 막대 단위 120 px = 1 GB. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 612
d = D(W, H, "BYTEBYTEGO · 04-01 §3",
      "4+2 이레이저 코딩: 조각 둘을 잃고 복원",
      "데이터 4조각에서 패리티 2조각을 계산하고, 조각 둘이 사라져도 남은 넷으로 되살립니다",
      "예시 입력 d1~d4 = 3 · 1 · 4 · 1")

CX0, CSTR, CW = 24, 224, 188
BX_PAD, BW, BH = 16, 156, 32
Y0, RSTR = 128, 40
titles = ["1 나눔", "2 패리티", "3 손실", "4 복원"]
names = ["d1", "d2", "d3", "d4", "p1", "p2"]
data_vals = {"d1": 3, "d2": 1, "d3": 4, "d4": 1}
par_vals = {"p1": 5, "p2": 3}

for k, t in enumerate(titles):
    x = CX0 + k * CSTR
    d.box(x, 92, CW, 28, PAPER2, RULE, 0.9, 6)
    d.t(x + CW / 2, 111, t, 13, INK, KR, "middle", 600)
    if k < 3:
        d.arrow([(x + CW + 4, 106), (x + CSTR - 4, 106)], MUTED, "ar", 1.3)

for k in range(4):
    x = CX0 + k * CSTR + BX_PAD
    for r, nm in enumerate(names):
        y = Y0 + r * RSTR
        is_par = nm.startswith("p")
        val = par_vals[nm] if is_par else data_vals[nm]
        label = f"{nm} = {val}"
        if is_par and k == 0:
            continue                      # 나눔 단계에는 패리티가 아직 없다
        if k == 2 and nm in ("d3", "d4"):
            d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="4" fill="{BAD}12" stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 3"/>')
            d.t(x + BW / 2, y + 21, f"{nm} 손실", 12, BAD, KR, "middle", 600)
            continue
        if k == 3 and nm in ("d3", "d4"):
            d.tone(x, y, BW, BH, ACC, 4, "14", 1.4)
            d.t(x + BW / 2, y + 21, label, 12, ACC, MONO, "middle", 600)
            continue
        c = WARN if is_par else INFO
        d.tone(x, y, BW, BH, c, 4, "12", 1.0)
        d.t(x + BW / 2, y + 21, label, 12, c, MONO, "middle", 600)

# 단계별 식
Y_F = Y0 + 6 * RSTR + 8
fx = CX0 + 1 * CSTR + BX_PAD
d.t(fx, Y_F + 12, "p1 = 3+2-4+4 = 5", 12, MUTED, MONO, "start")
d.t(fx, Y_F + 32, "p2 = -3+5+4-3 = 3", 12, MUTED, MONO, "start")
fx = CX0 + 3 * CSTR + BX_PAD
d.t(fx, Y_F + 12, "-d3+4·d4 = 5-3-2 = 0", 12, MUTED, MONO, "start")
d.t(fx, Y_F + 32, "d3-3·d4 = 3+3-5 = 1", 12, MUTED, MONO, "start")
d.t(fx, Y_F + 52, "d4 = 1 · d3 = 4", 12, ACC, MONO, "start", 600)

# 저장 공간 비교 막대: 1 GB = 120 px
BY = Y_F + 84
UNIT = 120
d.line(24, BY - 12, W - 48, BY - 12, RULE, 0.6)
d.t(24, BY + 18, "3 복제", 13, INK, KR, "start", 600)
for k in range(3):
    c = INFO if k == 0 else WARN
    d.tone(160 + k * UNIT + 2, BY, UNIT - 4, 28, c, 4, "14", 1.0)
    d.t(160 + k * UNIT + UNIT / 2, BY + 19, "1 GB", 12, c, MONO, "middle", 600)
d.t(160 + 3 * UNIT + 16, BY + 19, "3 GB", 12, INK, MONO, "start", 600)
BY2 = BY + 44
d.t(24, BY2 + 18, "4+2", 13, INK, MONO, "start", 600)
# 조각 하나 = 0.25 GB = 30 px
for k in range(6):
    x = 160 + k * 30
    c = WARN if k >= 4 else INFO
    d.tone(x + 1, BY2, 28, 28, c, 3, "22", 1.0)
d.t(160 + 6 * 30 + 16, BY2 + 19, "6 × 0.25 = 1.5 GB", 12, INK, MONO, "start", 600)

d.legend(H - 44, [("데이터", INFO), ("패리티 · 복사본", WARN), ("손실", BAD), ("복원된 조각", ACC)])
d.save("04-01.erasure-4plus2.svg")
