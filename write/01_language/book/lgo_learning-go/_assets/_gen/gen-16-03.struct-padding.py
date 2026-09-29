# 16-03.struct-padding — 세 구조체의 바이트 배치를 1바이트 칸으로 그린다. bool 이 int64 사이에 있으면 패딩이 늘어 24바이트, 모으면 16바이트
# 본문 요구(16-03 §1 「컴파일러는 정렬을 맞추려고 필드 사이와 끝에 패딩을 넣습니다」·원문 정오): BoolIntBool 24(0·8·16),
#           BoolBoolInt 16(0·1·8), IntBoolBool 16(0·8·9). 정오 확인용으로 struct{a,b,c bool} 은 3바이트(정렬값 1).
# 타입 스펙: type-layers 변형 — 행마다 바이트 칸 24개(칸 폭 28, 8바이트마다 굵은 경계). 필드는 색 칸, 패딩은 점선 빈 칸.
#           focal 은 가장 큰 BoolIntBool 의 패딩 14바이트.
# 사실 출처: Learning Go 2판 16장 「Using Sizeof and Offsetof」, go1.27.1 실행(2026-09-29) — 24 0 8 16 / 16 0 1 8 / 16 0 8 9, ThreeBools 3.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 470
X0, CW, CH = 236, 28, 36
Y0, PITCH = 140, 72


def row(i, name, size, fields):
    y = Y0 + i * PITCH
    d.t(X0 - 16, y + 16, name, 13, INK, MONO, "end", 600)
    d.t(X0 - 16, y + 32, f"{size} 바이트", 11, MUTED, KR, "end")
    used = set()
    for (lab, off, n, c) in fields:
        d.tone(X0 + off * CW, y, n * CW, CH, c, 3, "22", 1.1)
        d.t(X0 + off * CW + n * CW / 2, y + 23, lab, 11, c, MONO, "middle", 600)
        used.update(range(off, off + n))
    for b in range(size):
        if b not in used:
            d.o.append(f'<rect x="{X0 + b * CW + 2}" y="{y + 2}" width="{CW - 4}" height="{CH - 4}" rx="2" fill="none" stroke="{SOFT}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    for b in range(0, size + 1, 8):
        d.line(X0 + b * CW, y - 6, X0 + b * CW, y + CH + 6, MUTED if b % 8 == 0 else RULE, 1.2)
    pad = size - len(used)
    d.t(X0 + size * CW + 12, y + 23, f"패딩 {pad}", 11, ACC if pad >= 14 else MUTED, KR, "start", 600)


d = D(W, H, "LAYOUT · 16-03 §1",
      "필드 순서만 바꿔도 패딩이 줄어 구조체가 작아집니다",
      "세 구조체의 메모리 배치를 1바이트 칸으로 그렸다. 색 칸은 필드, 점선 칸은 컴파일러가 넣은 패딩이다. bool 두 개가 int64 앞뒤에 떨어져 있으면 각각 8바이트 칸을 차지해 24바이트가 되고, "
      "bool 둘을 모으면 16바이트다. 맨 아래 bool 셋만 있는 구조체는 가장 큰 정렬값이 1이라 패딩 없이 3바이트다. 굵은 세로선은 8바이트 경계다.",
      lead="색 칸은 필드, 점선 칸은 패딩입니다. 굵은 세로선은 8바이트 경계입니다.")

for k in range(0, 25, 8):
    d.t(X0 + k * CW, Y0 - 16, str(k), 11, MUTED, MONO, "middle")
row(0, "BoolIntBool", 24, [("b", 0, 1, INFO), ("i int64", 8, 8, OK), ("b2", 16, 1, INFO)])
row(1, "BoolBoolInt", 16, [("b", 0, 1, INFO), ("b2", 1, 1, INFO), ("i int64", 8, 8, OK)])
row(2, "IntBoolBool", 16, [("i int64", 0, 8, OK), ("b", 8, 1, INFO), ("b2", 9, 1, INFO)])
row(3, "struct{a,b,c bool}", 3, [("a", 0, 1, INFO), ("b", 1, 1, INFO), ("c", 2, 1, INFO)])

d.legend(414, [("bool 필드", INFO), ("int64 필드", OK), ("가장 많은 패딩", ACC)])
d.save("16-03.struct-padding.svg")
print("ok 16-03 struct-padding")
