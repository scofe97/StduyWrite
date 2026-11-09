# 15-02 §1 — 가용 파드 수가 바닥에 닿느냐
# 두 전략의 차이는 절차가 아니라 그 절차가 가용 수를 어디까지 떨어뜨리느냐다. 그러니
# 단계 나열이 아니라 가용 수를 세로 축으로 둔 두 줄이어야 한다.
# 타입 스펙: type-architecture.md — 상자에 든 것은 단계마다의 옛·새 파드 수다. 위와 같은 이유로 line 후보를 남겨 둔다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 630
d = D(W, H, "KUBERNETES IN ACTION · 15-02",
      "가용 수가 0 에 닿느냐가 갈림길이다",
      "두 전략 모두 옛 파드를 새 파드로 바꾼다. 다른 것은 그 과정에서 요청을 받을 수 있는 파드가 "
      "몇 개 남느냐다.")

lead = "replicas 3 · 0.5 → 0.6"
d.t(12, 74, lead, 12, MUTED, KR, "start")

def my_tag(d, cx, cy, txt, c, w=108):
    d.box(cx - w // 2, cy - 12, w, 24, fill=PAPER, stroke=c, sw=1.1, r=4)
    d.t(cx, cy + 4, txt, 12, c, KR, "middle", 600)

def strip(y0, label, steps, focal, verdict, vc):
    d.box(24, y0, W - 48, 206, PAPER2, RULE, 0.9, 8)
    d.t(36, y0 + 26, label, 13, INK, KR, "start", 600)
    BW = 126
    step_gap = 144
    start_x = 96
    for i, (t, old, new, avail) in enumerate(steps):
        cx = start_x + i * step_gap
        d.t(cx, y0 + 52, t, 12, SOFT, KR)
        d.box(cx - BW // 2, y0 + 64, BW, 72, PAPER2, RULE, 1.0, 6)
        d.t(cx, y0 + 88, f"0.5 × {old}", 12, MUTED, MONO)
        d.t(cx, y0 + 110, f"0.6 × {new}", 12, MUTED, MONO)
        col = OK if avail > 0 else ACC
        my_tag(d, cx, y0 + 162, f"가용 {avail}", col, 104)
        if i < len(steps) - 1:
            d.path(f"M {cx + BW // 2 + 3} {y0 + 100} L {cx + step_gap - BW // 2 - 7} {y0 + 100}", MUTED, 1.3, m="ar")
    # verdict column
    vx = 750
    d.line(660, y0 + 20, 660, y0 + 186, RULE, 0.8, "3 3")
    d.t(vx, y0 + 94, verdict, 13, vc, KR, "middle", 600)

strip(96, "Recreate — 전부 한꺼번에", [
    ("시작", 3, 0, 3), ("전부 종료", 0, 0, 0), ("전부 생성", 0, 3, 0), ("준비 완료", 0, 3, 3),
], True, "가용 0 구간이 생긴다", ACC)

strip(318, "RollingUpdate — 하나씩", [
    ("시작", 3, 0, 3), ("하나 교체", 2, 1, 3), ("둘 교체", 1, 2, 3), ("완료", 0, 3, 3),
], False, "가용 수가 유지된다", OK)

d.t(24, 538, "Recreate 는 옛 파드의 컨테이너가 다 끝난 뒤에야 새 파드를 만든다.", 12, MUTED, KR, "start")
d.t(24, 558, "그 사이 서비스가 멈추므로, 옛·새 버전이 동시에 돌면 안 되고 다운타임이 문제없을 때만 고른다.", 12, MUTED, KR, "start")

def my_legend(d, y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 100
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+10}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 12, MUTED, KR, "start")
        x += 44 + len(lab) * 14

my_legend(d, 580, [("요청을 받을 수 있다", OK), ("받을 수 없는 구간", ACC)])
d.save("15-02-recreate-vs-rollingupdate.svg")
print("ok")
