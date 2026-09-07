# 타입 스펙: type-sankey — 리본 두께 = 주소 개수. 3열 고정.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.2 Figure 4.21/4.22 + 주소 블록 표
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 1000, 580
d = D(W, H, "ADDRESS AGGREGATION · 200.23.16.0/20",
      "여덟 줄이 한 줄로, 예외 하나만 따로",
      "ISP 가 받은 /20 블록이 여덟 조직의 /23 으로 갈라졌다가 바깥 세상에는 두 개의 접두어로만 광고되는 흐름. 리본 두께는 주소 개수에 비례한다.",
      "리본 두께 = 주소 개수 · 4,096개를 256px 로 그렸습니다")

K = 0.0625        # px per address
BW = 12           # 노드 막대 두께
C1, C2, C3 = 180, 520, 800

d.t(C1 - 18, 92, "ISP 가 받은 블록", 11, SOFT, KR, "end", 600)
d.t(C2, 92, "여덟 조직에 나눈 /23", 11, SOFT, KR, "middle", 600)
d.t(C3 + 18, 92, "바깥에 광고되는 접두어", 11, SOFT, KR, "start", 600)

# --- 노드 좌표 (주소 수 → 높이) ---
src_top = 184                                   # 4096 → 256px, 184..440
c2 = [("Organization 0", "200.23.16.0/23 · 512", 512, 140),
      ("조직 2~7 여섯 곳", "6 x /23 · 3,072", 3072, 216),
      ("Organization 1", "200.23.18.0/23 · 512", 512, 452)]
c3 = [("Fly-By-Night 가 광고", "200.23.16.0/20 · 3,584", 3584, 168),
      ("ISPs-R-Us 가 광고", "200.23.18.0/23 · 512", 512, 424)]


def bar(x, y, n, focal=False):
    h = n * K
    d.o.append(f'<rect x="{x - BW / 2}" y="{y}" width="{BW}" height="{h}" rx="1" '
               f'fill="{ACC if focal else INK}" opacity="{0.95 if focal else 0.8}"/>')
    return h


def ribbon(y0, y1, h, focal=False):
    """왼쪽 열의 y0 에서 오른쪽 열의 y1 로 두께 h 의 리본. 제어점은 둘 다 중간 x."""
    mid = (C_FROM + C_TO) / 2
    a, b = C_FROM + BW / 2, C_TO - BW / 2
    dpath = (f"M {a} {y0} C {mid} {y0} {mid} {y1} {b} {y1} "
             f"L {b} {y1 + h} C {mid} {y1 + h} {mid} {y0 + h} {a} {y0 + h} Z")
    c, op = (ACC, "0.30") if focal else (MUTED, "0.18")
    d.o.append(f'<path d="{dpath}" fill="{c}" opacity="{op}"/>')


# --- 1열 → 2열 ---
C_FROM, C_TO = C1, C2
off = src_top
for nm, sub, n, y in c2:
    ribbon(off, y, n * K, focal=(nm == "Organization 1"))
    off += n * K

# --- 2열 → 3열 ---
C_FROM, C_TO = C2, C3
d3_off = c3[0][3]
for nm, sub, n, y in c2:
    if nm == "Organization 1":
        ribbon(y, c3[1][3], n * K, focal=True)
    else:
        ribbon(y, d3_off, n * K)
        d3_off += n * K

# --- 노드 막대 + 라벨 ---
bar(C1, src_top, 4096)
d.t(C1 - 18, src_top + 122, "Fly-By-Night-ISP", 12, INK, KR, "end", 600)
d.t(C1 - 18, src_top + 140, "200.23.16.0/20 · 4,096", 10, MUTED, MONO, "end")

for nm, sub, n, y in c2:
    bar(C2, y, n, focal=(nm == "Organization 1"))
    d.t(C2, y - 27, sub, 10, MUTED, MONO, "middle")
    d.t(C2, y - 12, nm, 12, ACC if nm == "Organization 1" else INK, KR, "middle", 600)

for i, (nm, sub, n, y) in enumerate(c3):
    focal = i == 1
    bar(C3, y, n, focal=focal)
    d.t(C3 + 18, y + n * K / 2 - 4, nm, 12, ACC if focal else INK, KR, "start", 600)
    d.t(C3 + 18, y + n * K / 2 + 14, sub, 10, MUTED, MONO, "start")

d.t(40, 512, "조직 1 의 주소는 ISP 블록 안에 있지만 다른 ISP 가 더 구체적인 /23 으로 광고합니다. "
              "바깥 라우터는 최장 접두어 일치로 그쪽을 고릅니다.", 11, MUTED, KR, "start")

d.legend(534, [("조직 1 의 예외 경로", ACC), ("집약되는 흐름", MUTED)])
d.t(960, 556, "WIDTH = ADDRESS COUNT · K = 0.0625 PX/ADDR", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.cidr-aggregation.svg"
d.save(out)

print("균형 검산")
print("  1열", 4096, "→ 2열", sum(n for _, _, n, _ in c2), "→ 3열", sum(n for _, _, n, _ in c3))
for nm, sub, n, y in c2:
    print(f"  {nm:<18}{n:>5} 주소 → {n * K:>5.0f}px  (y {y} ~ {y + n * K:.0f})")
print("→", out)
