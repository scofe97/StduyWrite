# 타입 스펙: type-data-flow — 단계마다 누가 무엇을 하는지. 같은 안테나 배열이 두 갈래 이득으로 갈린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.1 Figure 7.9(a)(b) —
#   신호 표기 y1 = H1,1(x) 와 두 방식의 이름은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 576
d = D(W, H, "SECTION 7.2.1 · MIMO",
      "같은 안테나로 확실하게 보낼지, 많이 보낼지",
      "안테나를 여럿 두면 이득이 두 갈래로 갈린다. 같은 정보를 여러 길로 보내거나, 다른 정보를 길마다 나눠 보낸다.",
      "신호 표기와 두 방식의 이름은 원문 Figure 7.9 의 것입니다")

COLS = [(24, 176), (248, 176), (472, 176), (696, 208)]
HEADS = ["보내는 것", "공중에서 벌어지는 일", "수신기가 하는 일", "얻는 것"]
for (x, w), head in zip(COLS, HEADS):
    d.t(x + w / 2, 106, head, 11, SOFT, KR)

ROWS = [
    (128, "공간 다이버시티", INFO, 1, 2,
     ["안테나 하나로", "정보 x 를 한 번"],
     ["위상을 맞춰 더하거나", "SNR 이 큰 쪽을 고릅니다"],
     ["같은 x 를 더 확실하게.", "다중경로 페이딩에 강해집니다.", "속도는 그대로입니다."]),
    (300, "공간 다중화", OK, 2, 2,
     ["안테나 둘로", "다른 정보 x₁·x₂ 를 함께"],
     ["식 둘 · 미지수 둘을", "풀어 x₁ 과 x₂ 를 분리"],
     ["한 번에 두 줄기가 흐릅니다.", "링크 속도 자체가 늘어납니다.", "경로가 서로 달라야 풉니다."]),
]
RH = 152
for ry, name, c, ntx, nrx, left, mid, right in ROWS:
    for x, w in COLS:
        d.box(x, ry, w, RH, PAPER2, RULE, 1.0)
    d.tone(COLS[3][0], ry, COLS[3][1], RH, ACC if name == "공간 다중화" else c, 6, "12", 1.2)
    d.t(COLS[0][0] + 16, ry + 26, name, 12, c, KR, "start", 600)
    for j, ln in enumerate(left):
        d.t(COLS[0][0] + 16, ry + 56 + j * 20, ln, 11, MUTED, KR, "start")

    cx0, cx1 = COLS[1][0] + 40, COLS[1][0] + 136
    txy = [ry + RH / 2 + (i - (ntx - 1) / 2) * 56 for i in range(ntx)]
    rxy = [ry + RH / 2 + (i - (nrx - 1) / 2) * 56 for i in range(nrx)]
    for a, ya in enumerate(txy):
        for b, yb in enumerate(rxy):
            d.line(cx0, ya, cx1, yb, c, 1.2)
    for ya in txy:
        d.o.append(f'<circle cx="{cx0}" cy="{ya}" r="5" fill="{c}"/>')
    for yb in rxy:
        d.o.append(f'<circle cx="{cx1}" cy="{yb}" r="5" fill="{c}"/>')
    d.t(cx0, ry + RH - 12, "송신", 10, SOFT, KR)
    d.t(cx1, ry + RH - 12, "수신", 10, SOFT, KR)
    d.t(COLS[1][0] + 88, ry + 24, "H 가 진폭과 위상을 바꿉니다", 10, SOFT, KR)

    for j, ln in enumerate(mid):
        d.t(COLS[2][0] + 16, ry + 60 + j * 20, ln, 11, MUTED, KR, "start")
    for j, ln in enumerate(right):
        d.t(COLS[3][0] + 16, ry + 48 + j * 22, ln, 11,
            ACC if name == "공간 다중화" else MUTED, KR, "start")

for ry, *_ in ROWS:
    for i in range(3):
        x1 = COLS[i][0] + COLS[i][1]
        d.arrow([(x1 + 8, ry + RH / 2), (COLS[i + 1][0] - 8, ry + RH / 2)], MUTED, "ar", 1.3)

d.t(24, 490, "수신 안테나를 N 개 두면 받는 총 전력이 대략 N 배가 되는 이득은 두 방식에 공통입니다.",
    11, MUTED, KR, "start")

d.legend(510, [("공간 다이버시티", INFO), ("공간 다중화", OK), ("속도가 늘어나는 쪽", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.mimo-two-gains.svg"
d.save(out)
print("→", out)
