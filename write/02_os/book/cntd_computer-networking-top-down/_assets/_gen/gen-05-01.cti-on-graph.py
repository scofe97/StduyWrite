# 타입 스펙: type-data-flow — 세 노드를 가로로 놓고 다음 홉 화살표가 마주 보는 순간을 세 컷으로 본다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 Figure 5.7(b)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

NX = {'y': 190, 'z': 500, 'x': 810}

W, H = 1000, 800
d = D(W, H, "SECTION 5.2.2 · COUNT TO INFINITY",
      "다음 홉이 서로를 가리키면 패킷이 갇힙니다",
      "x 를 목적지로 두고 y 와 z 의 다음 홉을 화살표로 그린 세 컷. 링크 비용이 오른 뒤 두 화살표가 마주 보며 라우팅 루프가 되고, z 가 직통으로 돌아설 때 풀린다.",
      "화살표는 x 로 가려고 그 노드가 고른 다음 홉입니다 — 마주 보면 패킷이 둘 사이를 오갑니다")

def cut(by, title, cyx, hop_y, hop_z, vy, vz, loop, cap):
    d.t(24, by - 58, title, 11, INK, KR, "start", 600)
    d.line(24, by - 48, 976, by - 48, RULE, 0.6, "3 6")
    # 노드
    for k, nx in NX.items():
        isx = k == 'x'
        d.box(nx - 42, by - 20, 84, 40, PAPER2, INFO if isx else RULE, 1.4 if isx else 1.0, 7)
        d.t(nx, by + 6, k, 13, INFO if isx else INK, MONO, "middle", 600)
    d.t(NX['x'], by - 30, "목적지", 11, INFO, KR)
    # 링크 — y·z 인접, z·x 인접, y·x 는 아래로 우회
    d.line(NX['y'] + 42, by, NX['z'] - 42, by, RULE, 1.0)
    d.line(NX['z'] + 42, by, NX['x'] - 42, by, RULE, 1.0)
    d.t(345, by - 8, "1", 11, SOFT, MONO)
    d.t(655, by - 8, "50", 11, SOFT, MONO)
    d.line(NX['y'], by + 20, NX['y'], by + 58, RULE, 1.0)
    d.line(NX['y'], by + 58, NX['x'], by + 58, RULE, 1.0)
    d.line(NX['x'], by + 58, NX['x'], by + 20, RULE, 1.0)
    d.t(500, by + 50, f"{cyx}", 11, BAD if cyx == 60 else SOFT, MONO)
    # 다음 홉 화살표 — 전부 수평
    c = BAD if loop else OK
    if hop_y == 'z':
        d.arrow([(NX['y'] + 46, by - 13), (NX['z'] - 46, by - 13)], c, "bad" if loop else "ok", 1.7)
    else:
        d.arrow([(NX['y'], by + 24), (NX['y'], by + 54), (NX['x'], by + 54), (NX['x'], by + 24)], OK, "ok", 1.7)
    if hop_z == 'y':
        d.arrow([(NX['z'] - 46, by + 13), (NX['y'] + 46, by + 13)], c, "bad" if loop else "ok", 1.7)
    else:
        d.arrow([(NX['z'] + 46, by), (NX['x'] - 46, by)], OK, "ok", 1.7)
    # 값
    d.t(NX['y'], by + 84, f"D_y(x) = {vy}", 11, c, MONO)
    d.t(NX['z'], by + 84, f"D_z(x) = {vz}", 11, c, MONO)
    d.t(24, by + 110, cap, 11, MUTED, KR, "start")

cut(170, "1. 사고 직전 — 각자 제 갈 길로 감", 4, 'x', 'y', "4", "5", False,
    "y 는 직통 링크로 바로 감 · z 는 y 를 거쳐 5  · 화살표가 마주 보지 않음")
cut(390, "2. c(y,x) 가 60 으로 오릅니다 — 두 화살표가 마주 봄", 60, 'z', 'y', "6", "7", True,
    "y 는 z 의 5 를 믿고 min{60, 1+5} = 6 을 냄 · 그런데 z 는 여전히 y 를 거침 · x 로 갈 패킷이 둘 사이를 오감")
cut(610, "3. z 가 직통으로 돌아섭니다 — 루프가 풀림", 60, 'z', 'x', "51", "50", False,
    "y 경유 값이 직통 50 을 넘는 순간 z 가 방향 전환 · 그때까지 둘은 번갈아 2 씩 올렸음")

d.legend(752, [("지금 쓰는 다음 홉", OK), ("마주 보는 루프", BAD), ("목적지", INFO)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.cti-on-graph.svg"
d.save(out)
print("→", out)
