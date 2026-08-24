# 01-01 §쿠버네티스 = 클러스터의 운영체제
# 본문·옛 도식: OS 가 앱과 하드웨어 사이를 중개하듯 쿠버네티스는 앱과 여러 서버 사이를
#   중개한다. 같은 3층 구조가 한 대에서 여러 대로 확장된다. 앱은 어느 서버가 자원을 내주는지
#   몰라도 된다.
# 타입 스펙: type-layers.md 를 두 벌 나란히 — 층 수가 같고 가운데 층만 바뀌는 것이 요점이라
#           두 스택의 층 높이·폭을 같게 두어야 그 대응이 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 612
d = D(W, H, "KUBERNETES IN ACTION · 01-01",
      "같은 3층 구조가 한 대에서 여러 대로 늘어난 것이다",
      "OS 가 앱과 하드웨어 사이를 중개하듯 쿠버네티스는 앱과 여러 서버 사이를 중개한다. "
      "가운데 층만 바뀌고 위아래 층의 역할은 그대로다.",
      lead="앱은 어느 서버가 자원을 내주는지 몰라도 된다 — 그것을 가운데 층이 감춘다")

LX, RX, SW = 270, 730, 380
TOP, LAYER_H, GAP = 224, 84, 12

ddx.band(d, 104, 556, "가운데 층이 바뀌었을 뿐 앱이 하는 일은 달라지지 않는다")

def stack(cx, title, layers):
    d.t(cx, 198, title, 13, INK, KR, "middle", 600)
    for i, (idx, name, sub, c) in enumerate(layers):
        y = TOP + i * (LAYER_H + GAP)
        d.o.append(f'<rect x="{cx-SW//2}" y="{y}" width="{SW}" height="{LAYER_H}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
        d.t(cx - SW // 2 + 16, y + 26, idx, 9, SOFT, MONO, "start")
        d.t(cx, y + 34, ddx.fit(name, 14, SW - 80, name), 14, c, KR, "middle", 600)
        d.t(cx, y + 58, ddx.fit(sub, 10, SW - 40, name), 10, SOFT, KR)

stack(LX, "컴퓨터 한 대", [
    ("L1", "애플리케이션", "돌려야 할 것", INFO),
    ("L2", "운영체제", "앱과 하드웨어를 중개한다 · 프로세스를 스케줄링한다", ACC),
    ("L3", "CPU · RAM · Disk", "한 대의 물리 자원", MUTED)])

stack(RX, "컴퓨터 클러스터 (여러 대)", [
    ("L1", "애플리케이션", "돌려야 할 것 — 그대로다", INFO),
    ("L2", "Kubernetes", "앱과 클러스터를 중개한다 · 노드에 스케줄링한다", ACC),
    ("L3", "Server · Server · Server", "여러 대의 물리 자원", MUTED)])

d.path(f"M {LX+SW//2+6} {TOP+LAYER_H+GAP+LAYER_H//2} L {RX-SW//2-10} {TOP+LAYER_H+GAP+LAYER_H//2}",
       ACC, 1.8, m="acc")
d.chip(500, TOP + LAYER_H + GAP + LAYER_H // 2, "같은 자리", ACC, 11)

# L3 층이 416~500 을 쓴다 — 산문은 그 아래로
d.t(36, 532, "층 수도 역할도 같고 다루는 자원의 개수만 다르다 — 그래서 클러스터의 운영체제라 부른다.",
     12, MUTED, KR, "start")
d.legend(572, [("돌려야 할 앱", INFO), ("중개하는 층", ACC)])
d.save("01-01-cluster-as-os.svg")
print("ok cluster-as-os")
