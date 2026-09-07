# 타입 스펙: type-line — 메시지 번호가 늘수록 광고 비용이 2씩 오르는 계단을 그대로 보인다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 Figure 5.7(b) 의 값으로 직접 모의
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, INFO, KR, MONO

# c(y,x) 가 4 에서 60 으로 오른 직후. c(y,z)=1, c(z,x)=50
CYX, CYZ, CZX = 60, 1, 50
Dy, Dz = 4, 5
log = [('y', min(CYX, CYZ + Dz))]          # 첫 메시지는 링크 변화를 알린 것
Dy = log[0][1]
turn = 'z'
while True:
    if turn == 'z':
        new = min(CZX, CYZ + Dy)
        if new == Dz:
            break
        Dz = new
        log.append(('z', Dz))
        turn = 'y'
    else:
        new = min(CYX, CYZ + Dz)
        if new == Dy:
            break
        Dy = new
        log.append(('y', Dy))
        turn = 'z'

SWITCH = next(i for i, (w, v) in enumerate(log) if w == 'z' and v == CZX)   # z 가 직통으로 돌아선 메시지

W, H = 1000, 620
d = D(W, H, "SECTION 5.2.2 · COUNT TO INFINITY",
      "나쁜 소식은 2씩 기어옵니다",
      "y-x 링크 비용이 4 에서 60 으로 오른 뒤 y 와 z 가 주고받은 광고를 메시지 단위로 모의한 그래프. 두 값이 번갈아 2씩 오르다 50 에 닿아서야 z 가 직통 링크를 다시 본다.",
      "좋은 소식은 두 번이면 끝났지만 나쁜 소식은 이만큼 걸립니다")

X0, X1, YB, YT = 92, 944, 470, 132
VMAX = 55
NM = len(log)


def px(m):
    return X0 + (m - 1) * (X1 - X0) / (NM - 1)


def py(v):
    return YB - v * (YB - YT) / VMAX


# 루프가 지속된 구간
d.o.append(f'<rect x="{px(2):.1f}" y="{YT - 4}" width="{px(SWITCH) - px(2):.1f}" '
           f'height="{YB - YT + 4:.1f}" fill="{ACC}0C"/>')

for v in (0, 10, 20, 30, 40, 50):
    d.line(X0, py(v), X1, py(v), RULE, 0.7)
    d.t(X0 - 12, py(v) + 4, str(v), 10, SOFT, MONO, "end")
for m in (1, 10, 20, 30, 40, NM):
    d.t(px(m), YB + 20, str(m), 10, SOFT, MONO)
d.t(30, 116, "광고된 비용", 11, MUTED, KR, "start")
d.t(X1, YB + 40, "메시지 번호", 11, MUTED, KR, "end")

# z 의 직통 링크 — 넘어서면 안 되는 선
d.line(X0, py(CZX), X1, py(CZX), BAD, 1.3, "6 4")
d.t(X0 + 8, py(CZX) - 10, f"c(z, x) = {CZX} · z 의 직통 링크", 11, BAD, KR, "start")

# 두 계열의 값이 1 씩 어긋나 선을 각각 그으면 한 줄로 겹쳐 보인다.
# 안내선은 하나만 긋고, 점 색으로 누가 보낸 광고인지 가른다.
allp = [(px(i + 1), py(v)) for i, (_, v) in enumerate(log)]
d.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in allp), MUTED, 1.0)
for i, (who, v) in enumerate(log):
    x, y = px(i + 1), py(v)
    d.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{ACC if who == "y" else INFO}"/>')

# 처음 여덟 메시지 — 번갈아 2 씩 오르는 모양을 확대해 보인다
d.t(140, 196, "처음 여덟 메시지", 11, MUTED, KR, "start")
for i, (who, v) in enumerate(log[:8]):
    cx = 168 + i * 62
    d.chip(cx, 222, f"{who} {v}", ACC if who == 'y' else INFO, 11, 8)
    if i < 7:
        d.path(f"M {cx + 22} 222 L {cx + 36} 222", SOFT, 1.0, m="soft")

sx, sy = px(SWITCH + 1), py(CZX)
d.o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6" fill="none" stroke="{BAD}" stroke-width="1.6"/>')
d.path(f"M {sx - 96} {sy - 54} L {sx - 10} {sy - 12}", BAD, 1.2, m="bad")
d.t(sx - 100, sy - 60, "z 가 via-y 를 51 로 계산하고 직통으로 돌아섭니다", 11, BAD, KR, "end")

d.t(px(2) + 8, YB - 16, f"루프가 지속된 {SWITCH - 1}개 메시지", 11, ACC, KR, "start")

d.t(30, 520, f"모의하면 메시지는 모두 {NM}개입니다. 링크 변화를 알린 첫 메시지를 빼고 z 가 돌아서기 "
             f"직전까지 세면 {SWITCH - 1}개이고, 원문이 적은 44 회가 이 셈입니다.", 11, MUTED, KR, "start")

d.legend(546, [("y 가 광고한 x 까지의 비용", ACC), ("z 가 광고한 비용", INFO), ("직통 링크 비용", BAD)])
d.t(960, 592, "KUROSE-ROSS 9E FIG 5.7(B) · SIMULATED", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.count-to-infinity.svg"
d.save(out)
print(f"메시지 {NM}개 · z 전환은 {SWITCH + 1}번째 · 첫 메시지 제외 전환 직전까지 {SWITCH - 1}개 →", out)
