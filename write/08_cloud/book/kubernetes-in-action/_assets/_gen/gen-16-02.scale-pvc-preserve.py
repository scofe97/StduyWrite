# 16-02 §3 — 파드는 지우고 PVC 는 남긴다
# 스케일다운·업을 따로 그리면 "번호로 되찾는다"가 안 보인다. 같은 번호 축 위에 두 단계를
# 겹쳐 놓아야 PVC 가 그 자리에 남아 있었다는 사실이 읽힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 764, "KUBERNETES IN ACTION · 16-02",
      "PVC 는 번호와 함께 그 자리에 남는다",
      "스케일다운은 파드만 지우고 PVC 는 그대로 둔다. 다시 올리면 각 파드가 ordinal 번호를 기준으로 "
      "이전과 같은 PVC 에 재부착된다.",
      "quiz 3 → 1 → 3 · 삭제는 높은 번호부터 역순")

ORD = (0, 1, 2)

def row(y0, label, pods, note, note_c):
    ddx.band(d, y0, y0 + 168, label, x=24, w=1172)
    for i, o in enumerate(ORD):
        cx = 260 + i * 300
        alive = pods[i]
        if alive:
            ddx.node(d, cx, y0 + 70, f"quiz-{o}", "Running", 200, 52, OK)
        else:
            ddx.node(d, cx, y0 + 70, f"quiz-{o}", "지워졌다", 200, 52, dim=True)
        d.line(cx, y0 + 98, cx, y0 + 112, RULE, 0.9, "3 4")
        ddx.node(d, cx, y0 + 136, f"db-data-quiz-{o}", "PVC — 남아 있다", 220, 48, ACC)
    d.t(1050, y0 + 100, note, 11, note_c, KR)

row(100, "① replicas 3 — 셋 다 도는 중", (True, True, True), "번호마다 전용 PVC", SOFT)
row(292, "② replicas 1 로 줄이면 — 역순으로 파드만 지운다", (True, False, False),
    "PVC 는 그대로 남는다", ACC)
row(484, "③ 다시 3 으로 올리면 — 같은 번호가 같은 PVC 를 되받는다", (True, True, True),
    "데이터가 이어진다", OK)

d.t(24, 692, "그 PVC 까지 지우려면 persistentVolumeClaimRetentionPolicy 를 따로 켜야 한다. "
                  "두 필드를 모두 Delete 로 두면 데이터가 사라진다.", 11, MUTED, KR, "start")
d.legend(716, [("도는 파드", OK), ("남아 있는 PVC", ACC)])
d.save("16-02-scale-pvc-preserve.svg")
print("ok")
