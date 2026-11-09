# 15-02 §6 — 0.7 의 신분이 바뀐다
# 본문이 "기다린다는 개념 자체가 없다"고 못박는다. 그러니 중간에 멈췄다 가는 그림이 아니라,
# 0.8 이 등장하는 순간 0.7 이 옛 것 쪽으로 넘어가는 장면이어야 한다.
# 타입 스펙: type-dp-security-matrix.md — 열이 ReplicaSet 셋, 행이 0.8 을 적기 전과 뒤. 중간 단계를 거치지 않는다는 것이
#           두 행의 차이로 드러난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 626
d = D(W, H, "KUBERNETES IN ACTION · 15-02",
      "기다린다는 개념 자체가 없다",
      "컨트롤러가 매 조정마다 하는 일은 현재 template 의 해시와 맞는 ReplicaSet 을 새 것으로 지목하고 "
      "나머지를 줄이는 것뿐이다. 0.8 을 적는 순간 지목 대상이 바뀐다.")

lead = "0.6 → 0.7 롤아웃이 절반쯤 진행됐을 때 0.8 을 적용"
d.t(12, 74, lead, 12, MUTED, KR, "start")

def scene(y0, label, rs, note, note_c, bw=184, start_cx=136, step_x=200, note_x=740):
    d.box(24, y0, W - 48, 206, PAPER2, RULE, 0.9, 8)
    d.t(36, y0 + 26, label, 13, INK, KR, "start", 600)
    for i, (ver, n, role, c) in enumerate(rs):
        cx = start_cx + i * step_x
        if c is ACC:
            d.o.append(f'<rect x="{cx - bw // 2}" y="{y0 + 58}" width="{bw}" height="96" rx="6" '
                       f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
            tc = ACC
        else:
            d.box(cx - bw // 2, y0 + 58, bw, 96, PAPER2, c, 1.1, 6)
            tc = c
        d.t(cx, y0 + 88, f"RS  {ver}", 14, tc, MONO, "middle", 600)
        d.t(cx, y0 + 114, f"replicas {n}", 12, MUTED, MONO)
        d.t(cx, y0 + 138, role, 12, tc, KR)
    
    d.line(note_x - 90, y0 + 20, note_x - 90, y0 + 186, RULE, 0.8, "3 3")
    d.t(note_x, y0 + 106, note, 12, note_c, KR, "middle")

scene(96, "0.8 을 적기 전", [
    ("0.6", "2 → 줄이는 중", "옛 것", WARN),
    ("0.7", "2 → 늘리는 중", "새 것", OK),
], "총합 4 · 상한 지킴", SOFT, bw=200, start_cx=180, step_x=230, note_x=710)

scene(318, "0.8 을 적은 뒤", [
    ("0.6", "→ 0", "옛 것", WARN),
    ("0.7", "→ 0", "옛 것이 됨", ACC),
    ("0.8", "→ 3", "새 것", OK),
], "총합 4 유지", SOFT, bw=184, start_cx=136, step_x=200, note_x=740)

d.t(24, 544, "0.7 을 완성한 뒤 0.8 로 넘어가지 않음 — 14-02 에서 이름 붙인 level-triggered 성질 · 중간값 0.7 을 거칠 의무 없음",
    12, MUTED, KR, "start")

def my_legend(d, y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 100
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+10}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 12, MUTED, KR, "start")
        x += 44 + len(lab) * 14

my_legend(d, 574, [("줄어드는 쪽", WARN), ("늘어나는 쪽", OK), ("신분이 바뀐 것", ACC)])
d.save("15-02-rollout-during-rollout.svg")
print("ok")
