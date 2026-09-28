# 15-03.bench-allocs — FileLen 벤치마크의 버퍼 크기별 allocs/op 를 go1.24.4 와 go1.27.1 로 견준 덤벨. 1·10바이트만 크게 달라진다
# 본문 요구(15-03 §2 「Go 1.25 부터 작은 버퍼는 스택에 놓입니다」): 버퍼 1·10바이트의 할당이 go1.24.4 에서 65,208·6,525회,
#           go1.27.1 에서 3회다. 100바이트 이상은 두 툴체인이 같다(657 · 70 · 11 · 5).
# 타입 스펙: type-bar Dumbbell — 가로, 행 여섯(pitch 52), 값축은 로그 눈금 1~100,000(한 자릿수 141.6px). 기준 계열은 빈 점(go1.24.4),
#           초점 계열은 채운 점(go1.27.1). 같은 값인 행은 두 점이 겹쳐 값 하나와 "같음" 을 적는다. 좌표는 반올림, 격자에 맞추지 않는다.
# 사실 출처: go1.24.4·go1.27.1 darwin/arm64(Apple M3) 에서 learning-go-book-2e/ch15 sample_code/bench 의 BenchmarkFileLen -benchmem (2026-09-28).
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 548
PX0, PX1 = 216, 924
DEC = (PX1 - PX0) / 5
Y0, PITCH = 148, 52


def px(v):
    return round(PX0 + math.log10(v) * DEC)


d = D(W, H, "DUMBBELL · 15-03 §2",
      "같은 코드도 Go 1.25 부터 작은 버퍼는 할당이 사라집니다",
      "FileLen 벤치마크를 버퍼 크기 여섯 가지로 돌린 한 번당 힙 할당 횟수. 빈 점은 go1.24.4, 채운 점은 go1.27.1 이다. "
      "1바이트는 65,208회에서 3회로, 10바이트는 6,525회에서 3회로 줄었고 100바이트 이상은 657 · 70 · 11 · 5회로 같다. "
      "Go 1.25 부터 크기가 변수인 작은 make 도 스택에 둘 수 있게 되어, 이 노트의 측정에서는 32바이트까지 힙 할당이 없었다.",
      lead="가로축은 로그 눈금입니다. 두 점이 겹친 행은 두 툴체인의 할당 횟수가 같습니다.")

rows = [("1 B", 65208, 3), ("10 B", 6525, 3), ("100 B", 657, 657), ("1,000 B", 70, 70), ("10,000 B", 11, 11), ("100,000 B", 5, 5)]
ybot = Y0 + PITCH * (len(rows) - 1)
for k in range(6):
    x = PX0 + round(k * DEC)
    d.line(x, Y0 - 20, x, ybot + 20, RULE, 0.8 if k else 1.0)
    d.t(x, ybot + 44, ["1", "10", "100", "1k", "10k", "100k"][k], 11, MUTED, MONO, "middle")
d.t((PX0 + PX1) / 2, ybot + 66, "allocs/op · 로그 눈금", 11, MUTED, KR, "middle")

for i, (lab, old, new) in enumerate(rows):
    y = Y0 + i * PITCH
    d.t(PX0 - 16, y + 4, lab, 12, INK, MONO, "end", 600)
    xo, xn = px(old), px(new)
    if old == new:
        d.o.append(f'<circle cx="{xo}" cy="{y}" r="7" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.5"/>')
        d.o.append(f'<circle cx="{xn}" cy="{y}" r="3.5" fill="{ACC}" stroke="{INK}" stroke-width="0.8"/>')
        d.t(xo + 16, y + 4, f"{old:,} · 같음", 11, MUTED, KR, "start")
    else:
        d.line(xn, y, xo, y, "rgba(245,245,245,0.40)", 1.0)
        d.o.append(f'<circle cx="{xo}" cy="{y}" r="6" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.5"/>')
        d.o.append(f'<circle cx="{xn}" cy="{y}" r="6" fill="{ACC}" stroke="{INK}" stroke-width="1"/>')
        d.t(xn - 14, y + 4, f"{new:,}", 11, ACC, MONO, "end", 600)
        d.t(xo + 14, y + 4, f"{old:,}", 11, MUTED, MONO, "start")

d.legend(492, [("go1.24.4 · 빈 점", MUTED), ("go1.27.1 · 채운 점", ACC)])
d.save("15-03.bench-allocs.svg")
print("ok 15-03 bench-allocs")
