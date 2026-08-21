# 15-02 §6 — 0.7 의 신분이 바뀐다
# 본문이 "기다린다는 개념 자체가 없다"고 못박는다. 그러니 중간에 멈췄다 가는 그림이 아니라,
# 0.8 이 등장하는 순간 0.7 이 옛 것 쪽으로 넘어가는 장면이어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 640, "KUBERNETES IN ACTION · 15-02",
      "기다린다는 개념 자체가 없다",
      "컨트롤러가 매 조정마다 하는 일은 현재 template 의 해시와 맞는 ReplicaSet 을 새 것으로 지목하고 "
      "나머지를 줄이는 것뿐이다. 0.8 을 적는 순간 지목 대상이 바뀐다.",
      "0.6 → 0.7 롤아웃이 절반쯤 진행됐을 때 0.8 을 적용")

def scene(y0, label, rs, note, note_c):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1152)
    for i, (ver, n, role, c) in enumerate(rs):
        cx = 220 + i * 300
        if c is ACC:
            d.o.append(f'<rect x="{cx-130}" y="{y0+72}" width="260" height="96" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
        else:
            d.box(cx - 130, y0 + 72, 260, 96, PAPER2, c, 1.1, 6); tc = c
        d.t(cx, y0 + 102, f"RS  {ver}", 13, tc, MONO, "middle", 600)
        d.t(cx, y0 + 126, f"replicas {n}", 11, MUTED, MONO)
        d.t(cx, y0 + 150, role, 11, tc, KR)
    d.t(1050, y0 + 120, note, 11, note_c, KR)

scene(100, "0.8 을 적기 전", [
    ("0.6", "2 → 줄이는 중", "옛 것", WARN),
    ("0.7", "2 → 늘리는 중", "새 것", OK),
], "총합 4 — 상한을 지킨다", SOFT)

scene(340, "0.8 을 적은 뒤", [
    ("0.6", "→ 0", "옛 것", WARN),
    ("0.7", "→ 0", "옛 것이 된다", ACC),
    ("0.8", "→ 3", "새 것", OK),
], "총합 4 그대로", SOFT)

d.t(24, 596, "0.7 을 완성한 뒤 0.8 로 넘어가지 않는다. 14-02 에서 이름 붙인 level-triggered 성질이 "
             "그대로 나타나는 자리라, 중간값 0.7 을 거쳐 갈 의무가 없다.", 11, MUTED, KR, "start")
d.legend(618 - 4, [("줄어드는 쪽", WARN), ("늘어나는 쪽", OK), ("신분이 바뀐 것", ACC)])
d.save("15-02-rollout-during-rollout.svg")
print("ok")
