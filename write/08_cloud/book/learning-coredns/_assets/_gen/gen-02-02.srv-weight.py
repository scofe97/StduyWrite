# 02-02 §4 — SRV 의 가중치는 같은 우선순위 안에서 클라이언트를 나누는 비율이다.
# 원문 근거: Example 2-14 의 api.bar.example — "SRV 100 200 80 api1.bar.example"(2/3),
#            "SRV 100 100 8080 api2.bar.example"(1/3), "SRV 200 100 8080 api1.foo.example"
#            (앞의 둘이 모두 안 될 때). "All of the weights of targets at the same priority are added;
#            each target should receive a share of clients in proportion to its weight relative to the sum."
# 타입 스펙: type-sankey — 띠 굵기가 곧 나뉘는 양이고, 가중치 비율이 이 도식의 논지다.
#           우선순위 200 의 폴백은 평상시 흐르는 양이 0 이라 띠로 그리지 않고 주석으로 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 940, 556
d = D(W, H, "LEARNING COREDNS · 02-02 §4",
      "가중치는 같은 우선순위 안에서만 나눈다",
      "클라이언트는 먼저 가장 낮은 우선순위 값을 가진 대상들만 후보로 삼는다. "
      "그 안에서 가중치의 합 대비 자기 몫만큼 나눠 가지므로, 200 과 100 이면 2 대 1 이 된다.",
      "띠의 굵기가 곧 클라이언트의 비율입니다")

K = 0.8                      # px per client-unit — 300 단위 = 240px
X1, X2, X3 = 200, 470, 740
BAR_W = 12
TOP = 176

for x, head in ((X1, "CLIENTS"), (X2, "PRIORITY 100"), (X3, "TARGET")):
    d.t(x, 124, head, 8, SOFT, MONO)

def bar(x, y, h):
    d.o.append(f'<rect x="{x - BAR_W / 2}" y="{y}" width="{BAR_W}" height="{h}" fill="{INK}"/>')

def band(xa, ya, xb, yb, h, color, op):
    mx = (xa + xb) / 2
    dpath = (f"M {xa} {ya} C {mx} {ya} {mx} {yb} {xb} {yb} "
             f"L {xb} {yb + h} C {mx} {yb + h} {mx} {ya + h} {xa} {ya + h} Z")
    d.o.append(f'<path d="{dpath}" fill="{color}" fill-opacity="{op}"/>')

# 리본을 먼저, 그 위에 막대와 라벨
band(X1 + BAR_W / 2, TOP, X2 - BAR_W / 2, TOP, 240, MUTED, 0.18)
band(X2 + BAR_W / 2, TOP, X3 - BAR_W / 2, TOP, 160, ACC, 0.28)
band(X2 + BAR_W / 2, TOP + 160, X3 - BAR_W / 2, TOP + 176, 80, MUTED, 0.18)

bar(X1, TOP, 240)
bar(X2, TOP, 240)
bar(X3, TOP, 160)
bar(X3, TOP + 176, 80)

d.t(X1 - 16, TOP + 124, "클라이언트 전체", 12, INK, KR, "end", 600)
d.t(X1 - 16, TOP + 142, "300", 9, MUTED, MONO, "end")

d.t(X2, TOP - 30, "우선순위 100 후보군", 12, INK, KR, "middle", 600)
d.t(X2, TOP - 14, "300", 9, MUTED, MONO)

d.t(X3 + 16, TOP + 74, "api1.bar.example", 12, ACC, MONO, "start", 600)
d.t(X3 + 16, TOP + 92, "가중치 200 · 2/3", 12, MUTED, KR, "start")
d.t(X3 + 16, TOP + 210, "api2.bar.example", 12, INK, MONO, "start", 600)
d.t(X3 + 16, TOP + 228, "가중치 100 · 1/3", 12, MUTED, KR, "start")

d.t(20, 464, "우선순위 200 의 api1.foo.example 은 평상시 몫이 없다 — 앞의 둘이 모두 실패해야 후보가 된다", 13, MUTED, KR, "start")

d.legend(488, [("가중치가 큰 쪽이 받는 몫", ACC)])
d.save("02-02.srv-weight.svg")
