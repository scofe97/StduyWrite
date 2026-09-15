# 타입 스펙: type-data-flow — 거짓말이 닿는 방향과 정보가 도는 방향이 반대라 고리가 길면 뚫린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 독 뿌린 역경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 1000, 815
d = D(W, H, "SECTION 5.2.2 · POISONED REVERSE",
      "거짓말은 거쳐 가는 이웃 하나에게만 합니다",
      "독 뿌린 역경로가 두 노드 루프는 막고 세 노드 고리는 못 막는 이유. 거짓말은 자기가 지금 거쳐 가는 이웃 한 쪽으로만 가고, 반대 방향은 열려 있다.",
      "막는 방향과 정보가 도는 방향이 서로 반대입니다")

def node(nx, by, k, c=RULE, w=84):
    d.box(nx - w/2, by - 20, w, 40, PAPER2, c, 1.4 if c != RULE else 1.0, 7)
    d.t(nx, by + 6, k, 13, INK if c == RULE else c, MONO, "middle", 600)

# ── 위: 두 노드 루프는 막힙니다
BY = 210
d.t(24, BY - 78, "두 노드가 맞물린 루프 — 막힘", 11, OK, KR, "start", 600)
d.line(24, BY - 68, 976, BY - 68, RULE, 0.6, "3 6")
NA = {'y': 210, 'z': 520, 'x': 830}
for k, nx in NA.items():
    node(nx, BY, k, INFO if k == 'x' else RULE)
d.t(NA['x'], BY - 30, "목적지", 11, INFO, KR)
d.line(NA['y'] + 42, BY, NA['z'] - 42, BY, RULE, 1.0)
d.line(NA['z'] + 42, BY, NA['x'] - 42, BY, RULE, 1.0)
d.arrow([(NA['z'] - 46, BY - 15), (NA['y'] + 46, BY - 15)], BAD, "bad", 1.7, dash="5 4")
d.t(365, BY - 26, "D_z(x) = 무한대  (거짓말)", 11, BAD, MONO)
d.arrow([(NA['z'] + 46, BY + 15), (NA['x'] - 46, BY + 15)], OK, "ok", 1.7)
d.t(675, BY + 34, "z 는 실제로 y 를 거침", 11, MUTED, KR)
d.t(24, BY + 68, "z 는 x 로 갈 때 y 경유 → y 에게 \"x 까지 무한대\" 광고 · y 는 z 를 거칠 생각을 하지 않음", 11, MUTED, KR, "start")
d.t(24, BY + 90, "그래서 c(y,x) 가 올라도 y 는 직통 값을 그대로 쓰고, z 는 곧장 자기 직통으로 옮겨 감 · 2 씩 오르는 왕복이 생기지 않음", 11, MUTED, KR, "start")

# ── 아래: 세 노드 고리는 뚫립니다
BY2 = 520
d.t(24, BY2 - 78, "세 노드가 고리를 이루면 — 뚫림", 11, BAD, KR, "start", 600)
d.line(24, BY2 - 68, 976, BY2 - 68, RULE, 0.6, "3 6")
NB = {'y': 210, 'z': 520, 'w': 830}
for k, nx in NB.items():
    node(nx, BY2, k)
d.line(NB['y'] + 42, BY2, NB['z'] - 42, BY2, RULE, 1.0)
d.line(NB['z'] + 42, BY2, NB['w'] - 42, BY2, RULE, 1.0)
d.line(NB['y'], BY2 + 20, NB['y'], BY2 + 62, RULE, 1.0)
d.line(NB['y'], BY2 + 62, NB['w'], BY2 + 62, RULE, 1.0)
d.line(NB['w'], BY2 + 62, NB['w'], BY2 + 20, RULE, 1.0)
d.t(520, BY2 + 54, "고리가 닫힘", 11, SOFT, KR)
d.arrow([(NB['z'] + 46, BY2 - 15), (NB['w'] - 46, BY2 - 15)], BAD, "bad", 1.7, dash="5 4")
d.t(675, BY2 - 26, "z 가 막은 상대는 w", 11, BAD, KR)
d.arrow([(NB['z'] - 46, BY2 + 15), (NB['y'] + 46, BY2 + 15)], OK, "ok", 1.7)
d.t(365, BY2 + 34, "y 에게는 유한한 값 그대로 광고", 11, OK, KR)
d.t(24, BY2 + 96, "y 가 z 를 거친다는 사실 자체가 z 가 y 에게 유한한 값을 줬다는 뜻 · 그 광고를 막는 쪽이 없습니다 — z 가 입을 막은 상대는 w 이지 y 가 아니기 때문", 11, MUTED, KR, "start")
d.t(24, BY2 + 118, "w → z 와 y → w 도 같은 이유로 열려 있어, 잘못된 값이 고리를 거꾸로 한 바퀴 돌아 제자리로 옴", 11, MUTED, KR, "start")

d.tone(300, 700, 400, 32, BAD, 7, "12", 1.3)
d.t(500, 721, "거짓말은 한 방향, 정보는 반대 방향", 11, BAD, KR, "middle", 600)

d.legend(752, [("무한대라는 거짓말", BAD), ("막히지 않은 광고", OK), ("목적지", INFO)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.poisoned-reverse.svg"
d.save(out)
print("→", out)
