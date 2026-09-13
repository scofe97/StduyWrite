# 08-01 §3 — 128KB 요청이 order 5 에서 빗나갔을 때 무슨 일이 일어나는가.
# 본문의 mermaid 를 대체한다 — 노드 9개로 일회성 단순 흐름 범위를 넘고, 이 편의 핵심 메커니즘이라 정적 SVG 로 옮겼다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 아래로 내려갈수록 상위 order 를 뒤진다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 696
MX, MW = 248, 288
RX, RW = 600, 352
CX = MX + MW / 2

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-01 §3",
       "없으면 위에서 빌려 쪼갭니다",
       "드라이버가 128KB 를 요청하면 32 페이지, 곧 order 5 다. order 5 리스트가 비어 있으면 할당자는 실패하지 않고 상위 order 청크를 하나 가져와 반으로 쪼갠다. 쪼갠 두 조각이 buddy block 이고, 한쪽은 요청자에게 다른 쪽은 하위 order 리스트로 간다.",
       "청크가 물리 연속이라 반으로 쪼개도 두 조각이 각각 물리 연속입니다")

def node(y, h, title, sub, c, focal=False):
    if focal:
        d.tone(MX, y, MW, h, ACC, 8, "12", 1.4)
    else:
        d.box(MX, y, MW, h, PAPER2, RULE, 1.0, 8)
    d.t(CX, y + (26 if sub else h / 2 + 5), title, 13, ACC if focal else (c if c else INK), KR, "middle", 600)
    if sub:
        d.t(CX, y + 46, sub, 13, MUTED, KR)

def exit_box(y, h, title, sub, sub2, c):
    d.tone(RX, y, RW, h, c, 8, "12", 1.1)
    d.t(RX + 16, y + 26, title, 13, c, KR, "start", 600)
    if sub:
        d.t(RX + 16, y + 46, sub, 13, MUTED, KR, "start")
    if sub2:
        d.t(RX + 16, y + 66, sub2, 13, MUTED, KR, "start")

Y = [116, 204, 292, 400]
node(Y[0], 56, "128KB 요청 = 32 페이지 = order 5", None, INFO)
node(Y[1], 56, "order 5 리스트에 청크가 있나?", None, WARN)
node(Y[2], 56, "order 6 리스트에 청크가 있나?", None, WARN)
node(Y[3], 72, "order 6 청크를 반으로 쪼갠다", "256KB 하나 → 128KB buddy block 둘", None, True)

for i, (y0, h0) in enumerate([(Y[0], 56), (Y[1], 56), (Y[2], 56)]):
    top = y0 + h0
    c = ACC if i == 2 else MUTED
    d.arrow([(CX, top + 4), (CX, Y[i + 1] - 6)], c, "acc" if i == 2 else "ar", 1.4)
    if i in (1, 2):
        d.chip(CX - 76, top + 16, "비었다", SOFT, 13)

exit_box(Y[1], 56, "dequeue 해서 주고 끝난다", "쪼갤 일이 없습니다", None, OK)
exit_box(Y[2], 56, "상위 order 로 계속 올라간다", "order 10 까지 비면 할당 실패 — 드문 일입니다", None, WARN)

for i, y0 in enumerate([Y[1], Y[2]]):
    mid = y0 + 28
    c = OK if i == 0 else WARN
    d.arrow([(MX + MW + 4, mid), (RX - 6, mid)], c, "ok" if i == 0 else "warn", 1.4)
    d.chip((MX + MW + RX) / 2, mid - 22, "있다" if i == 0 else "없다", c, 13)

# 쪼갠 두 조각의 행방 — 한 줄기가 둘로 갈린다
SY = 516
LCX, RCX = MX - 112 + 120, MX + 176 + 120
d.line(CX, Y[3] + 72, CX, 492, ACC, 1.4)
d.line(LCX, 492, RCX, 492, ACC, 1.4)
d.arrow([(LCX, 492), (LCX, SY - 6)], OK, "ok", 1.4)
d.arrow([(RCX, 492), (RCX, SY - 6)], INFO, "info", 1.4)
d.tone(MX - 112, SY, 240, 56, OK, 8, "12", 1.1)
d.t(LCX, SY + 32, "절반은 요청자에게", 13, OK, KR)
d.tone(MX + 176, SY, 240, 56, INFO, 8, "12", 1.1)
d.t(RCX, SY + 32, "절반은 order 5 에 enqueue", 13, INFO, KR)

d.t(24, 612, "해제할 때는 거꾸로입니다. 128KB 를 free 하면 buddy 를 먼저 찾고, 찾으면 256KB 로 병합해 order 6 에 넣습니다 — 이것이 defrag 입니다.", 13, MUTED, KR, "start")

d.legend(H - 56, [("바로 끝나는 길", OK), ("분기", WARN), ("쪼개는 길 — 이 절의 논점", ACC), ("하위 order 로", INFO)])
d.save("08-01.split-cascade.svg")
print("ok 08-01.split-cascade")
