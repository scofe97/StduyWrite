# 10-02 §1 — 만드는 순서가 뒤집힌다
# 동적과 정적의 차이는 기능이 아니라 순서다. 그러니 두 순서를 나란히 놓아야 "운영자가 먼저"라는
# 말이 무엇을 뜻하는지 보인다.
# 타입 스펙: type-process.md — 두 밴드가 같은 슬롯의 세 단계를 반복하되 순서가 뒤집혀 있고, 각 단계 위에 그 일을 하는
#           주체(개발자 · 운영자 · 프로비저너 · 컨트롤 플레인)가 적힌다.
#           type-process 정본의 입력 계약은 역할 레인 1~6 이 전제인데 이 그림에 레인은 없다.
#           주체를 요구하지 않는 유일한 라우팅 규칙이 semantic-patterns 의
#           "Stage framework with semantic slots" 한 줄이라 그것을 근거로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1240, 660, "KUBERNETES IN ACTION · 10-02",
      "누가 먼저 만드는가",
      "동적 프로비저닝은 요구가 오면 그때 만든다. 정적 프로비저닝은 운영자가 PV 를 미리 만들어 두고, "
      "나중에 온 PVC 가 그중 맞는 것을 찾아 바인딩된다.",
      "이미 있는 스토리지를 클러스터에 들일 때 쓴다")

def order(y0, label, steps, c, focal):
    ddx.band(d, y0, y0 + 200, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    BW, GP = 240, 44
    X0 = 90
    CX = [X0 + BW // 2 + i * (BW + GP) for i in range(len(steps))]
    for cx, (t, s, who) in zip(CX, steps):
        d.t(cx, y0 + 62, who, 10, SOFT, KR)
        ddx.node(d, cx, y0 + 118, t, s, BW, 76, c)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+BW//2+5} {y0+118} L {b-BW//2-9} {y0+118}", MUTED, 1.4, m="ar")

order(100, "동적 — 요구가 먼저", [
    ("PVC", "요구를 적는다", "개발자"), ("StorageClass", "방법을 고른다", "미리 정해 둠"),
    ("PV", "그때 만들어진다", "프로비저너"),
], INFO, False)

order(324, "정적 — PV 가 먼저", [
    ("PV", "미리 만들어 둔다", "운영자"), ("PVC", "나중에 요구한다", "개발자"),
    ("바인딩", "맞는 것을 찾아 묶는다", "컨트롤 플레인"),
], ACC, True)

d.t(24, 560, "정적에서는 PVC 의 요구(용량·access mode·클래스)에 맞는 PV 가 없으면 Pending 에 머문다. "
             "동적처럼 없으면 만들어 주는 주체가 없기 때문이다.", 11, MUTED, KR, "start")
d.t(24, 582, "storageClassName 을 빈 문자열로 두면 동적 프로비저닝을 끄고 미리 만든 PV 만 후보로 삼는다.",
     11, MUTED, KR, "start")
d.legend(612, [("요구가 먼저", INFO), ("실체가 먼저", ACC)])
d.save("10-02-static-provisioning.svg")
print("ok")
