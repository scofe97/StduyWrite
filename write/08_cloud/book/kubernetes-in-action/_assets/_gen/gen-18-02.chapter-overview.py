# 18-02 전체 지도 — 파드 하나를 넘어설 때
# 본문이 "층과 층은 앞의 결정이 다음 질문을 부르는 순서로 이어진다"고 못박는다. 그러니 층을
# 나란히 두는 데서 그치면 안 되고, 층 사이에 다음 질문을 잇는 화살표가 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 704, "KUBERNETES IN ACTION · 18-02",
      "파드 하나를 넘어설 때 정할 것",
      "몇 번 성공해야 하고 동시에 몇 개를 돌릴지 정하면, 그다음 실패를 어느 수준에서 다룰지가 따라온다. "
      "그것이 정해지면 파드를 구분할지가 남는다.",
      "§1 몇 번·몇 개 · §2·§3 실패 · §4 구분 · §5 판단")

LAYERS = [("§1  몇 번 · 몇 개", ("completions", "몇 번 성공하면 끝인가"),
           ("parallelism", "동시에 몇 개를 돌릴까"), INFO,
           "그러면 실패는 어떻게 다루나"),
          ("§2·§3  실패", ("restartPolicy", "같은 파드에서? 새 파드로?"),
           ("backoffLimit", "몇 번까지 버틸까"), INFO,
           "그러면 파드를 구분해야 하나"),
          ("§4  구분", ("completionMode", "NonIndexed ↔ Indexed"),
           ("인덱스", "각자 다른 몫을 맡는다"), ACC, None)]
for i, (label, a, b, c, next_q) in enumerate(LAYERS):
    y = 108 + i * 176
    ddx.band(d, y, y + 128, label, x=24, w=1152, focal=(c is ACC), bar=ACC if c is ACC else None)
    for j, (t, s) in enumerate((a, b)):
        cx = 400 + j * 420
        d.box(cx - 190, y + 44, 380, 64, "#161B22", c, 1.1, 6)
        d.t(cx - 170, y + 70, t, 12, c, MONO, "start", 600)
        d.t(cx - 170, y + 92, s, 10, MUTED, KR, "start")
    if next_q:
        d.path(f"M 600 {y+132} L 600 {y+172}", ACC, 1.4, m="acc")
        d.t(616, y + 158, next_q, 11, ACC, KR, "start")

d.t(24, 636, "각 층은 왼쪽에서 오른쪽으로 읽는다. 층과 층은 앞의 결정이 다음 질문을 부르는 순서로 이어진다.",
     11, MUTED, KR, "start")
d.legend(656 - 4, [("정할 것", INFO), ("마지막 갈림", ACC)])
d.save("18-02.chapter-overview.svg")
print("ok")
