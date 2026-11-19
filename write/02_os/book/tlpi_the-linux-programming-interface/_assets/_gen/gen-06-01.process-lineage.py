# 06-01 §4 「getppid() 와 init 으로 이어지는 족보」 — 부모 번호(PPid)를 따라 올라가면 init(PID 1)에 닿는다.
# 본문 근거: 이 노트 「4. 부모 프로세스와 프로세스 트리」 첫 소절.
# 값 근거: 840·1200·1250 은 사슬을 보이려고 정한 예시 번호다.
# 공식 근거: TLPI 6.2 — 모든 프로세스는 부모가 있고 부모를 거슬러 올라가면 프로세스 1 init 에 닿는다. pstree(1) 이 이 트리를 보인다.
#           proc_pid_status(5) — PPid 는 부모 프로세스의 PID 다.
# 타입 스펙: type-tree — 뿌리를 왼쪽에 두고 자식을 오른쪽으로 편다. 연결은 직각, focal 은 뿌리 init 하나.
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, INK, MUTED, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 336
d = D(W, H, "TLPI · 06-01 §4",
      "PPid 를 따라 올라가면 init 에 닿는다",
      "각 프로세스는 부모의 PID 를 PPid 로 갖고, 부모를 거듭 따라가면 PID 1 인 init 에 닿는다.",
      "init 에서 sshd, bash, worker 로 이어지는 부모-자식 사슬과 PPid 값")

NW, NH, Y = 184, 68, 124
xs = [24, 264, 504, 744]
nodes = [("init (PID 1)", "모든 프로세스의 조상", ACC), ("sshd (PID 840)", "PPid 1", None),
         ("bash (PID 1200)", "PPid 840", None), ("worker (PID 1250)", "PPid 1200", None)]
for k in range(3):
    d.arrow([(xs[k] + NW + 4, Y + NH / 2), (xs[k + 1] - 6, Y + NH / 2)], MUTED, "ar", 1.4)
for x, (t1, t2, c) in zip(xs, nodes):
    if c:
        d.tone(x, Y, NW, NH, c, 6, "18", 1.4)
    else:
        d.box(x, Y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + NW / 2, Y + 30, t1, 14, INK, MONO, "middle", 600)
    d.t(x + NW / 2, Y + 52, t2, 13, MUTED, MONO if t2.startswith('PPid') else KR)

# 아래: 자식에서 뿌리로 거슬러 오르는 길
bx_from, bx_to, by = xs[3] + NW / 2, xs[0] + NW / 2, 236
d.path(f"M {bx_from} {Y + NH + 6} V {by - 12} Q {bx_from} {by} {bx_from - 12} {by} H {bx_to + 12} "
       f"Q {bx_to} {by} {bx_to} {by - 12} V {Y + NH + 8}", INFO, 1.5, m="info")
d.chip((bx_from + bx_to) / 2, by, "PPid 를 따라 올라감 (/proc)", INFO, 13)

d.legend(H - 52, [("뿌리 (전체의 조상)", ACC), ("거슬러 오르는 길", INFO)])
d.save("06-01.process-lineage.svg")
print("ok 06-01 process-lineage")
