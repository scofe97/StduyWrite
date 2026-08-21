# 18-02 §2 — 어느 수준에서 다시 하느냐
# 캡션이 두 흐름을 구체적으로 준다 — OnFailure 는 같은 파드에서 컨테이너를, Never 는 새 파드를.
# 그러니 결과만 비교하면 안 되고 무엇이 다시 만들어지는지가 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 700, "KUBERNETES IN ACTION · 18-02",
      "컨테이너를 다시 띄우나, 파드를 새로 만드나",
      "같은 실패인데 다시 하는 단위가 다르다. 하나는 파드를 그대로 두고 그 안에서, "
      "다른 하나는 파드를 실패로 두고 컨트롤러가 새로 만든다.",
      "backoffLimit 은 어느 쪽이든 재시도 횟수를 묶는다")

def flow(y0, label, steps, c, focal, who):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1192, focal=focal, bar=ACC if focal else None)
    BW, GP = 250, 44
    X0 = 120
    CX = [X0 + BW // 2 + i * (BW + GP) for i in range(len(steps))]
    for cx, (t, s) in zip(CX, steps):
        d.box(cx - BW // 2, y0 + 72, BW, 84, PAPER2, c, 1.1, 6)
        d.t(cx, y0 + 104, ddx.fit(t, 12, BW - 16, t), 12, c, KR, "middle", 600)
        d.t(cx, y0 + 130, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+BW//2+5} {y0+114} L {b-BW//2-9} {y0+114}", MUTED, 1.4, m="ar")
    d.t(1080, y0 + 114, who, 11, c, KR)

flow(100, "restartPolicy: OnFailure", [
    ("컨테이너 실패", "exit 1"), ("같은 파드 안에서", "컨테이너만 다시"),
    ("파드는 그대로", "이름·IP 가 유지된다"),
], INFO, False, "kubelet 이 한다")

flow(340, "restartPolicy: Never", [
    ("컨테이너 실패", "exit 1"), ("파드가 Failed 로", "그 파드는 끝난다"),
    ("새 파드를 만든다", "이름·IP 가 바뀐다"),
], ACC, True, "Job 컨트롤러가 한다")

d.t(24, 596, "그래서 실패한 파드의 로그를 보고 싶다면 Never 가 낫다 — 실패한 파드가 그대로 남기 때문이다. "
             "OnFailure 는 같은 파드 안에서 덮어쓴다.", 11, MUTED, KR, "start")
d.t(24, 618, "어느 쪽이든 backoffLimit 을 넘으면 Job 자체가 실패로 표시되고 더 만들지 않는다.",
     11, MUTED, KR, "start")
d.legend(652, [("kubelet 수준", INFO), ("컨트롤러 수준", ACC)])
d.save("18-02-restart-policy-failure.svg")
print("ok")
