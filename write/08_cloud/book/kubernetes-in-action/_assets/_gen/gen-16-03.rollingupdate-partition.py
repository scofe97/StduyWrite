# 16-03 §2 — 경계선 하나가 세 가지 쓰임을 만든다
# partition 을 "일부만 업데이트"로만 그리면 staging 과 canary 가 왜 같은 필드인지 안 보인다.
# 값을 옮겨 가며 세 상태를 나란히 놓아야 한 축의 눈금이라는 게 읽힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 768, "KUBERNETES IN ACTION · 16-03",
      "경계선을 어디에 긋느냐가 전부다",
      "partition 값보다 ordinal 이 낮은 파드는 업데이트되지 않는다. 그 값을 replica 수 이상에 두면 "
      "아무것도 안 바뀌고, 하나만 넘겨 두면 canary 가 된다.",
      "replicas 5 · quiz-0 ~ quiz-4 · 업데이트는 높은 번호부터")

ORD = range(5)

def row(y0, label, part, note, note_c, focal):
    ddx.band(d, y0, y0 + 168, label, x=24, w=1172)
    for o in ORD:
        cx = 180 + o * 190
        new = o >= part
        c = ACC if (new and focal) else (OK if new else SOFT)
        ddx.node(d, cx, y0 + 96, f"quiz-{o}", "새 버전" if new else "옛 버전", 150, 60,
                 c if new else None, dim=not new)
    if 0 < part <= 5:
        lx = 180 + part * 190 - 95
        d.line(lx, y0 + 44, lx, y0 + 148, ACC, 1.6, "6 4")
        d.t(lx + 8, y0 + 40, f"partition {part}", 10, ACC, MONO, "start")
    elif part > 5:
        d.t(1140, y0 + 40, f"partition {part}", 10, ACC, MONO, "end")
    d.t(610, y0 + 152, note, 11, note_c, KR)

row(100, "partition 5 — staging · 롤아웃 미발동", 5, "준비만 하고 발동하지 않는다", SOFT, False)
row(292, "partition 4 — canary 하나만", 4, "한 대만 새 버전으로 시험한다", ACC, True)
row(484, "partition 0 — 전부 교체", 0, "기본값과 같아진다", OK, False)

d.t(24, 690, "StatefulSet 은 kubectl rollout pause 를 지원하지 않는다. partition 이 그 효과를 대신하되, "
                 "멈추는 지점을 번호로 지정할 수 있어 그 이상을 준다.", 11, MUTED, KR, "start")
d.legend(716, [("옛 버전 유지", SOFT), ("새 버전", OK), ("경계선과 canary", ACC)])
d.save("16-03-rollingupdate-partition.svg")
print("ok")
