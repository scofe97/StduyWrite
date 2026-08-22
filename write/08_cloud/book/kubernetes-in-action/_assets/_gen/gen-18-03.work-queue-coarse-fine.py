# 18-03 §1 — 파드 하나가 몇 개를 집는가
# 캡션이 두 방식을 "아이템 하나 vs 큐가 빌 때까지"로 가른다. 그러니 큐 그림 하나로는 부족하고,
# 파드가 집는 횟수가 눈에 띄게 달라야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 704, "KUBERNETES IN ACTION · 18-03",
      "하나만 집고 끝나는가, 빌 때까지 집는가",
      "일을 미리 나누지 않고 파드가 큐에서 꺼내 쓴다. 파드 하나가 아이템 하나만 처리하고 끝나는지, "
      "큐가 빌 때까지 계속 꺼내는지가 두 방식을 가른다.",
      "일의 크기와 개수가 방식을 정한다")

def scene(y0, label, per_pod, completions, note, c, focal):
    ddx.band(d, y0, y0 + 240, label, x=24, w=1192, focal=focal, bar=ACC if focal else None)
    d.box(90, y0 + 68, 200, 148, PAPER, RULE, 0.9, 8)
    d.t(190, y0 + 94, "큐", 11, SOFT, KR)
    for i in range(4):
        d.box(112, y0 + 116 + i * 26, 156, 20, PAPER2, RULE, 0.9, 3)
    d.t(190, y0 + 230, "아이템들", 10, SOFT, KR)
    d.path(f"M 296 {y0+116} L 366 {y0+116} L 366 {y0+64} L 980 {y0+64}", c, 1.2)
    for j in range(3):
        cx = 480 + j * 250
        ddx.node(d, cx, y0 + 116, f"파드 {j+1}", per_pod, 220, 62, c)
        d.path(f"M {cx} {y0+64} L {cx} {y0+81}", c, 1.2, m="ok" if c is OK else "acc")
        d.t(cx, y0 + 176, completions, 10, MUTED, KR)
    # x=1090 은 파드 3 상자의 오른쪽 변이라 글자 절반이 상자 안에 들어갔다. 옆에는 폭이
    # 157px 짜리 글이 들어갈 자리(126px)가 없으므로 띠 오른쪽 위로 올린다.
    d.t(1192, y0 + 40, note, 11, c, KR, "end")

scene(100, "coarse — 아이템 하나에 파드 하나", "아이템 1 개 처리", "처리하면 끝난다",
      "completions 를 아이템 수만큼", OK, False)
scene(364, "fine — 파드가 큐를 비운다", "빌 때까지 계속", "큐를 확인하고 또 꺼낸다",
      "completions 없이 parallelism 만", ACC, True)

d.t(24, 636, "coarse 는 아이템 수를 미리 알아야 completions 를 적을 수 있다. fine 은 그것을 몰라도 되지만, "
             "파드가 '큐가 비었다'를 스스로 판단해 끝내야 한다.", 11, MUTED, KR, "start")
d.legend(656, [("한 번 집는다", OK), ("빌 때까지", ACC)])
d.save("18-03-work-queue-coarse-fine.svg")
print("ok")
