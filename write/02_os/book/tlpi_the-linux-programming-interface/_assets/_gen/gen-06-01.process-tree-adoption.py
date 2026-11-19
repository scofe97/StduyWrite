# 06-01 §4 「부모의 종료와 init 으로의 입양」 — bash 가 먼저 종료되면 worker 의 부모가 bash 에서 init 으로 바뀌고 PPid 가 1 이 된다.
# 본문 근거: 이 노트 「4. 부모 프로세스와 프로세스 트리」 둘째 소절.
# 값 근거: 840·1200·1250 은 설명용 예시 번호다(process-lineage 와 같음). subreaper 가 없다고 가정한다.
# 공식 근거: TLPI 6.2 — 부모가 종료돼 고아가 되면 init 이 입양하고 이후 getppid() 는 1 을 반환한다.
#           PR_SET_CHILD_SUBREAPER(2const) — subreaper 가 있으면 가장 가까운 살아 있는 subreaper 가 새 부모가 된다.
# 타입 스펙: type-architecture-delta — Before · 변경 내역 · After 세 칸. 같은 좌표를 쓰고 REMOVED·REWIRED·CHANGED 를 글자와 선 모양으로 보인다.
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, INK, MUTED, INFO, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 516
d = D(W, H, "TLPI · 06-01 §4",
      "부모 bash 가 죽으면 worker 는 init 에 입양된다",
      "부모 종료 전에는 init 에서 worker 까지 한 줄이고, 종료 뒤에는 bash 가 사라지며 worker 의 부모가 init 으로 바뀐다.",
      "bash 종료 전후의 부모 연결과 PPid 값 비교")

PY, PH, PWD = 104, 336, 304
BX, AX, LX, LW = 24, 632, 344, 272
NX, NW, NH, STR = 52, 200, 52, 72
names = [("init (PID 1)", "모든 프로세스의 조상"), ("sshd (PID 840)", "PPid 1"),
         ("bash (PID 1200)", "PPid 840"), ("worker (PID 1250)", "PPid 1200")]
ny = [PY + 56 + i * STR for i in range(4)]


def panel(x0, title):
    d.box(x0, PY, PWD, PH, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 16, PY + 28, title, 14, INK, KR, "start", 600)
    d.line(x0 + 12, PY + 40, x0 + PWD - 12, PY + 40, RULE, 0.8)


def node(x0, i, sub=None, c=None, ghost=False):
    x, y = x0 + NX, ny[i]
    col = c or RULE
    if ghost:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{PAPER}" stroke="{BAD}" '
                   f'stroke-width="1.2" stroke-dasharray="5 4"/>')
    elif c:
        d.tone(x, y, NW, NH, c, 6, "18", 1.4)
    else:
        d.box(x, y, NW, NH, PAPER, RULE, 1.0, 6)
    tcol = MUTED if ghost else INK
    d.t(x + NW / 2, y + 22, names[i][0], 14, tcol, MONO, "middle", 600)
    d.t(x + NW / 2, y + 42, sub or names[i][1], 12, MUTED, MONO if (sub or names[i][1]).startswith('PPid') else KR)


def vlink(x0, i, c=MUTED, dash=None, mk="ar"):
    cx = x0 + NX + NW / 2
    d.arrow([(cx, ny[i] + NH + 2), (cx, ny[i + 1] - 4)], c, mk, 1.4, dash)


# Before
panel(BX, "부모 종료 전")
for i in range(4):
    node(BX, i, c=BAD if i == 2 else None)
for i in range(3):
    vlink(BX, i)

# After
panel(AX, "부모 종료 후")
node(AX, 0, sub="입양한 새 부모")
node(AX, 1)
node(AX, 2, sub="종료됨", ghost=True)
node(AX, 3, sub="PPid 1", c=INFO)
vlink(AX, 0)
vlink(AX, 1, BAD, "4 3", "bad")
vlink(AX, 2, BAD, "4 3", "bad")
# init → worker 로 옮겨진 연결(왼쪽으로 돌아 내려간다)
lx = AX + 24
yi, yw = ny[0] + NH / 2, ny[3] + NH / 2
d.path(f"M {AX + NX - 4} {yi} H {lx + 12} Q {lx} {yi} {lx} {yi + 12} V {yw - 12} Q {lx} {yw} {lx + 12} {yw} H {AX + NX - 6}",
       ACC, 1.6, m="acc")

# 변경 내역
d.box(LX, PY, LW, PH, PAPER2, RULE, 1.0, 6)
d.t(LX + 16, PY + 28, "변경 내역", 14, INK, KR, "start", 600)
d.line(LX + 12, PY + 40, LX + LW - 12, PY + 40, RULE, 0.8)
ledger = [("REMOVED", BAD, "bash (PID 1200)", "부모 프로세스가 종료됨"),
          ("REWIRED", ACC, "worker 의 부모 연결", "bash 에서 init 으로 이동"),
          ("CHANGED", INFO, "worker 의 PPid", "1200 에서 1 로 바뀜")]
for k, (tag, c, l1, l2) in enumerate(ledger):
    ly = PY + 72 + k * 84
    d.t(LX + 16, ly, tag, 13, c, MONO, "start", 600)
    d.t(LX + 16, ly + 22, l1, 13, INK, KR, "start")
    d.t(LX + 16, ly + 42, l2, 12, MUTED, KR, "start")
    if k < 2:
        d.line(LX + 12, ly + 58, LX + LW - 12, ly + 58, RULE, 0.8)

d.legend(H - 52, [("종료됨 (REMOVED)", BAD), ("연결이 바뀜 (REWIRED)", ACC), ("값이 바뀜 (CHANGED)", INFO)])
d.save("06-01.process-tree-adoption.svg")
print("ok 06-01 process-tree-adoption")
