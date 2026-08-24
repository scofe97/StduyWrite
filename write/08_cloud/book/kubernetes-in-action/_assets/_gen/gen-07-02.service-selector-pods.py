# 07-02 §Service 는 이름이 아니라 label selector 로 고른다
# 본문·옛 도식: selector 와 label 이 맞는 Pod 에게만 트래픽이 가고, 멤버가 바뀌어도 selector 가
#   자동으로 따라간다. Service 는 Pod 이름을 하나도 모른다. 새로 뜬 payment-3 도 label 만
#   맞으면 자동으로 편입된다. 같은 메커니즘을 Deployment 와 nodeSelector 도 쓴다.
# 타입 스펙: 맞는 것과 안 맞는 것이 갈리는 판정이 요점이라, 같은 목록 안에서 통과와 탈락을
#           색으로 가른다. 이름이 아니라 라벨로 걸린다는 사실은 '이름을 모른다' 를 적어 못 박는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 620
d = D(W, H, "KUBERNETES IN ACTION · 07-02",
      "Service 는 Pod 이름을 하나도 모른다",
      "selector 에 적힌 라벨을 가진 Pod 만 트래픽을 받는다. 나중에 뜬 Pod 도 그 라벨을 "
      "갖자마자 자동으로 편입되고, 라벨이 다르면 같은 namespace 에 있어도 제외된다.",
      lead="같은 메커니즘을 Deployment 와 nodeSelector 도 그대로 쓴다")

SVC = (160, 340)
PODS = [(660, 246), (660, 340), (660, 434), (660, 528)]
PW, PH = 400, 76

ddx.band(d, 104, 564, "이름으로 걸지 않으므로 멤버가 바뀌어도 selector 를 고칠 일이 없다")

d.o.append(f'<rect x="{SVC[0]-120}" y="{SVC[1]-70}" width="240" height="140" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SVC[0], SVC[1] - 34, "Service", 14, ACC, KR, "middle", 600)
d.t(SVC[0], SVC[1] - 4, "selector:", 11, SOFT, MONO)
d.t(SVC[0], SVC[1] + 18, "app=payment", 13, ACC, MONO, "middle", 600)
d.t(SVC[0], SVC[1] + 46, "이름은 적혀 있지 않다", 10, SOFT, KR)

ROWS = [("payment-1", "app=payment", True, "라벨이 맞는다"),
        ("payment-2", "app=payment", True, "라벨이 맞는다"),
        ("order-1", "app=order", False, "라벨이 다르다 → 제외"),
        ("payment-3", "app=payment", True, "나중에 떴지만 자동 편입")]
for (cx, cy), (name, lab, hit, note) in zip(PODS, ROWS):
    c = OK if hit else BAD
    d.box(cx - PW // 2, cy - PH // 2, PW, PH, PAPER2, c, 1.1, 6)
    d.t(cx - PW // 2 + 20, cy - 8, name, 13, c, MONO, "start", 600)
    d.t(cx - PW // 2 + 20, cy + 16, lab, 11, MUTED, MONO, "start")
    d.t(cx + PW // 2 - 20, cy + 5, note, 10, SOFT, KR, "end")

SPINE = 400
d.path(f"M {SVC[0]+120+6} {SVC[1]} L {SPINE} {SVC[1]}", ACC, 1.8)
d.path(f"M {SPINE} {PODS[0][1]} L {SPINE} {PODS[3][1]}", MUTED, 1.4)
for (cx, cy), (_, _, hit, _) in zip(PODS, ROWS):
    c = OK if hit else BAD
    d.path(f"M {SPINE} {cy} L {cx-PW//2-10} {cy}", c, 1.5, m="ok" if hit else "bad")

d.t(36, 524, "라벨만 맞으면 이름을 몰라도 편입된다 — 그것이 Pod 를 갈아 끼워도 Service 를 "
             "안 고쳐도 되는 이유다.", 12, MUTED, KR, "start")
d.legend(580, [("selector 에 걸린 Pod", OK), ("라벨이 달라 제외된 Pod", BAD),
               ("거는 쪽", ACC)])
d.save("07-02-service-selector-pods.svg")
print("ok service-selector-pods")
