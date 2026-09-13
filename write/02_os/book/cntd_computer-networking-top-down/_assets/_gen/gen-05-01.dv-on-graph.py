# 타입 스펙: type-data-flow — 세 노드를 가로로 놓고 벡터가 오가는 방향과 그때 바뀌는 값을 세 컷으로 본다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 Figure 5.6
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

NX = {'y': 190, 'x': 500, 'z': 810}

W, H = 1000, 850
d = D(W, H, "SECTION 5.2.2 · DISTANCE VECTOR EXCHANGE",
      "이웃에게 건넨 벡터가 남의 표를 고칩니다",
      "c(x,y)=2 · c(x,z)=7 · c(y,z)=1 인 세 노드에서 거리 벡터가 오가며 x 와 z 의 추정이 7 에서 3 으로 내려가고, 더 보낼 것이 없어 멈추는 세 컷.",
      "화살표는 건네진 거리 벡터입니다 — 값이 바뀐 노드만 다시 건넵니다")

def cut(by, title, vecs, hot, send, cap):
    d.t(24, by - 58, title, 11, INK, KR, "start", 600)
    d.line(24, by - 48, 976, by - 48, RULE, 0.6, "3 6")
    for k, nx in NX.items():
        c = ACC if k in hot else RULE
        d.box(nx - 44, by - 20, 88, 40, PAPER2, c, 1.4 if k in hot else 1.0, 7)
        d.t(nx, by + 6, k, 13, ACC if k in hot else INK, MONO, "middle", 600)
        d.t(nx, by - 30, f"D_{k} = {vecs[k]}", 11, ACC if k in hot else MUTED, MONO)
    # 링크 — y·x 인접, x·z 인접, y·z 는 아래로 우회
    d.line(NX['y'] + 44, by, NX['x'] - 44, by, RULE, 1.0)
    d.line(NX['x'] + 44, by, NX['z'] - 44, by, RULE, 1.0)
    d.t(345, by - 8, "2", 11, SOFT, MONO)
    d.t(655, by - 8, "7", 11, SOFT, MONO)
    d.line(NX['y'], by + 20, NX['y'], by + 56, RULE, 1.0)
    d.line(NX['y'], by + 56, NX['z'], by + 56, RULE, 1.0)
    d.line(NX['z'], by + 56, NX['z'], by + 20, RULE, 1.0)
    d.t(500, by + 48, "1", 11, SOFT, MONO)
    # 건네진 벡터 — 전부 수평
    for a, b, off in send:
        if (a, b) in (('y','x'), ('x','y')):
            x1, x2 = (NX['y'] + 48, NX['x'] - 48) if a == 'y' else (NX['x'] - 48, NX['y'] + 48)
            d.arrow([(x1, by + off), (x2, by + off)], ACC, "acc", 1.6)
        elif (a, b) in (('x','z'), ('z','x')):
            x1, x2 = (NX['x'] + 48, NX['z'] - 48) if a == 'x' else (NX['z'] - 48, NX['x'] + 48)
            d.arrow([(x1, by + off), (x2, by + off)], ACC, "acc", 1.6)
    d.t(24, by + 88, cap, 11, MUTED, KR, "start")

cut(180, "라운드 0 — 직통 비용만 압니다",
    {'y': "[2,0,1]", 'x': "[0,2,7]", 'z': "[7,1,0]"}, set(), [],
    "x 는 z 까지 직통 7 로 알고 있습니다. y 를 거치면 더 싸다는 것을 아직 모릅니다.")

cut(400, "라운드 1 — 서로 건네고, 받은 값으로 다시 풉니다",
    {'y': "[2,0,1]", 'x': "[0,2,3]", 'z': "[3,1,0]"}, {'x', 'z'},
    [('y','x',-14), ('x','y',14), ('x','z',-14), ('z','x',14)],
    "x 는 y 가 준 [2,0,1] 을 보고 min{2+1, 7+0} = 3 을 냅니다. z 도 같은 이유로 3 이 됩니다. y 만 그대로입니다.")

cut(620, "라운드 2 — 바뀐 x·z 만 건넵니다",
    {'y': "[2,0,1]", 'x': "[0,2,3]", 'z': "[3,1,0]"}, set(),
    [('x','y',-14), ('x','z',-14), ('z','x',14)],
    "y 는 보낼 것이 없어 가만히 있습니다. 받은 쪽도 값이 바뀌지 않아 여기서 멈춥니다 — 조용한 상태입니다.")

d.tone(660, 700, 300, 30, OK, 6, "12", 1.2)
d.t(810, 720, "조용한 상태(quiescent)", 11, OK, KR)

d.t(24, 752, "최소를 낸 이웃이 그대로 다음 홉입니다. x 가 z 로 갈 때 다음 홉은 z 가 아니라 y 이고, 식을 푸는 순간 답과 전달 표가 함께 나옵니다.", 11, INFO, KR, "start")

d.legend(786, [("건네진 거리 벡터", ACC), ("값이 바뀐 노드", ACC), ("멈춘 상태", OK)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.dv-on-graph.svg"
d.save(out)
print("→", out)
