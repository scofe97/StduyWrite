# 타입 스펙: type-data-flow — 같은 고리 망이 회차마다 시계와 반시계로 뒤집히는 두 상태.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.1 Figure 5.5
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

REL = {'w': (220, 54), 'x': (66, 164), 'z': (374, 164), 'y': (220, 274)}
RING = (('w','x'), ('x','y'), ('y','z'), ('z','w'))

W, H = 1000, 730
d = D(W, H, "SECTION 5.2.1 · ROUTE OSCILLATION",
      "떠난 자리가 공짜가 되어 다시 그리로 몰립니다",
      "네 노드가 고리를 이루고 x·y·z 가 모두 w 로 보내는 망에서 링크 비용을 그 링크의 부하와 같게 두면, 트래픽이 두 상태를 회차마다 오가며 멈추지 않는다.",
      "링크 비용이 곧 그 링크가 지금 나르는 양입니다 — 비면 싸지고 몰리면 비싸집니다")

def panel(px, title, heavy_side, cap):
    d.box(px, 150, 440, 360, f"{INK}05", RULE, 1.0, 10)
    d.t(px + 220, 138, title, 11, INK, KR, "middle", 600)
    heavy = (('y','z'), ('z','w')) if heavy_side == 'ccw' else (('y','x'), ('x','w'))
    for a, b in RING:
        (x1, y1), (x2, y2) = REL[a], REL[b]
        pair = (a, b) if (a, b) in heavy else (b, a)
        hot = pair in heavy
        d.line(px + x1, 166 + y1, px + x2, 166 + y2, ACC if hot else INFO, 2.8 if hot else 1.1)
    for k, (x, y) in REL.items():
        isw = k == 'w'
        d.box(px + x - 22, 166 + y - 16, 44, 32, PAPER2, INFO if isw else RULE, 1.4 if isw else 1.0, 6)
        d.t(px + x, 166 + y + 5, k, 12, INFO if isw else INK, MONO, "middle", 600)
    d.t(px + 220, 186, "목적지", 11, INFO, KR)
    hx = px + (352 if heavy_side == 'ccw' else 88)
    lx = px + (88 if heavy_side == 'ccw' else 352)
    d.t(hx, 268, "몰려서 비쌈", 11, ACC, KR)
    d.t(lx, 268, "비어서 공짜", 11, INFO, KR)
    d.t(px + 220, 470, cap, 11, MUTED, KR)

panel(20, "회차 N — 반시계로 쏠림", 'ccw',
      "시계 쪽이 비어 공짜 · 다음 회차에 다들 그리로 감")
panel(540, "회차 N+1 — 시계로 쏠림", 'cw',
      "이번엔 반시계가 비어 공짜 · 그다음 회차에 되돌아감")

d.arrow([(474, 300), (526, 300)], BAD, "bad", 1.6)
d.arrow([(526, 344), (474, 344)], BAD, "bad", 1.6)
d.t(500, 290, "한 회차", 11, BAD, KR)
d.t(500, 372, "마다 뒤집힘", 11, BAD, KR)

d.tone(300, 528, 400, 34, BAD, 7, "12", 1.3)
d.t(500, 550, "지금 싸다 = 곧 비싸진다", 11, BAD, KR, "middle", 600)

d.t(20, 596, "y 가 시계로 옮기면 x-w 링크가 그만큼 비싸지고, 비어 버린 y-z·z-w 는 그 순간 싸짐 · 다음 회차에 그것을 본 셋이 다 같이 되돌아감", 11, MUTED, KR, "start")
d.t(20, 618, "같은 값 → 같은 판단 → 함께 이동 → 옮겨 간 자리가 곧바로 비싸짐", 11, MUTED, KR, "start")
d.t(20, 640, "처방은 링크 광고 시각에 무작위를 섞는 것 · 따로 돌기 시작해도 결국 발이 맞아 버리기 때문입니다(자기 동기화).", 11, INFO, KR, "start")

d.legend(672, [("몰려서 비싸진 링크", ACC), ("비어서 공짜가 된 링크", INFO), ("회차마다 뒤집힘", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.oscillation.svg"
d.save(out)
print("→", out)
