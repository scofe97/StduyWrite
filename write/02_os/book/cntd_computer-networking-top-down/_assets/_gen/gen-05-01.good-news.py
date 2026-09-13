# 타입 스펙: type-data-flow — 비용이 내려가는 소식은 알림 두 번으로 끝난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 Figure 5.7(a)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

NX = {'y': 190, 'z': 500, 'x': 810}

W, H = 1000, 830
d = D(W, H, "SECTION 5.2.2 · GOOD NEWS TRAVELS FAST",
      "내려가는 소식은 두 번 만에 끝납니다",
      "c(y,x) 가 4 에서 1 로 내려갔을 때 y 가 알리고 z 가 고쳐 알리면 더 바뀔 것이 없어 멈추는 세 컷. 값이 내려가는 방향에서는 아무도 남의 옛 값에 기대지 않는다.",
      "화살표는 이웃에게 보낸 알림입니다 — 두 번 오가고 멈춥니다")

def cut(by, title, cyx, notify, vy, vz, hot, cap):
    d.t(24, by - 58, title, 11, INK, KR, "start", 600)
    d.line(24, by - 48, 976, by - 48, RULE, 0.6, "3 6")
    for k, nx in NX.items():
        isx = k == 'x'
        c = ACC if k in hot else (INFO if isx else RULE)
        d.box(nx - 42, by - 20, 84, 40, PAPER2, c, 1.4 if (isx or k in hot) else 1.0, 7)
        d.t(nx, by + 6, k, 13, ACC if k in hot else (INFO if isx else INK), MONO, "middle", 600)
    d.t(NX['x'], by - 30, "목적지", 11, INFO, KR)
    d.line(NX['y'] + 42, by, NX['z'] - 42, by, RULE, 1.0)
    d.line(NX['z'] + 42, by, NX['x'] - 42, by, RULE, 1.0)
    d.t(345, by - 8, "1", 11, SOFT, MONO)
    d.t(655, by - 8, "50", 11, SOFT, MONO)
    d.line(NX['y'], by + 20, NX['y'], by + 58, RULE, 1.0)
    d.line(NX['y'], by + 58, NX['x'], by + 58, RULE, 1.0)
    d.line(NX['x'], by + 58, NX['x'], by + 20, RULE, 1.0)
    d.t(500, by + 50, str(cyx), 11, OK if cyx == 1 else SOFT, MONO)
    if notify == 'y2z':
        d.arrow([(NX['y'] + 46, by - 13), (NX['z'] - 46, by - 13)], ACC, "acc", 1.7)
        d.t(345, by - 24, "D_y(x) = 1", 11, ACC, MONO)
    elif notify == 'z2y':
        d.arrow([(NX['z'] - 46, by + 13), (NX['y'] + 46, by + 13)], ACC, "acc", 1.7)
        d.t(345, by + 30, "D_z(x) = 2", 11, ACC, MONO)
    d.t(NX['y'], by + 86, f"D_y(x) = {vy}", 11, ACC if 'y' in hot else MUTED, MONO)
    d.t(NX['z'], by + 86, f"D_z(x) = {vz}", 11, ACC if 'z' in hot else MUTED, MONO)
    d.t(24, by + 112, cap, 11, MUTED, KR, "start")

cut(170, "1. 사고 직전", 4, None, "4", "5", set(),
    "y 는 직통 4 로 갑니다. z 는 y 를 거쳐 5 입니다.")
cut(390, "2. c(y,x) 가 1 로 내려갑니다 — y 가 알립니다", 1, 'y2z', "1", "5", {'y'},
    "y 가 min{1+0, 1+5} = 1 을 내고 값이 바뀌었으므로 z 에게 보냅니다.")
cut(610, "3. z 가 고쳐 알리면 끝납니다", 1, 'z2y', "1", "2", {'z'},
    "z 는 min{50, 1+1} = 2 로 내리고 y 에게 보냅니다. y 는 받아 봐도 바뀔 것이 없어 아무 말도 하지 않습니다.")

d.t(24, 748, "값이 내려가는 쪽에서는 아무도 남의 옛 값에 기대지 않습니다. 자기 직통이 싸졌다는 사실만으로 답이 정해지므로 두 번의 반복으로 끝납니다.", 11, INFO, KR, "start")

d.legend(772, [("보낸 알림", ACC), ("값이 바뀐 노드", ACC), ("목적지", INFO)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.good-news.svg"
d.save(out)
print("→", out)
