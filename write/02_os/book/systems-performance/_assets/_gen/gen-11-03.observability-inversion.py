# 11-03 §5 — VM 과 컨테이너는 관측 가능한 방향이 서로 뒤집혀 있다.
# 타입 스펙: type-dp-security-matrix — 두 기술 × 두 자리(호스트·게스트)의 되고 안 되는 격자다.
#           축약: 보안 격자가 아니라 관측 가능 여부 격자로 문법만 빌린다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 476
COL_W, ROW_H, X0, Y0 = 356, 92, 176, 156

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-03 §5",
       "관측이 뒤집힌다 — VM 과 컨테이너",
       "같은 자리에서 보이는 것이 두 기술에서 정반대다. VM 게스트는 커널을 다 보지만 물리 자원을 못 보고, 컨테이너 게스트는 커널을 못 보는데 호스트 통계가 새어 든다.",
       "그래서 관측은 컨테이너가 호스트 운영자에게, VM 이 엔드유저에게 유리합니다")

# 헤더
d.t(X0 + COL_W / 2, Y0 - 16, "하드웨어 VM (11-02)", 14, INK, KR, "middle", 600)
d.t(X0 + COL_W + 24 + COL_W / 2, Y0 - 16, "컨테이너 (11-03)", 14, INK, KR, "middle", 600)

ROWS = [
    ("호스트에서", [("자원은 보이나 게스트 내부는 못 봄", WARN), ("모든 컨테이너 프로세스를 다 봄", OK)]),
    ("게스트에서", [("자체 커널이라 커널 추적이 다 됨", OK), ("커널 추적 불가 · 호스트 통계가 새어 듦", ACC)]),
]

for r, (label, cells) in enumerate(ROWS):
    y = Y0 + r * (ROW_H + 16)
    d.t(X0 - 20, y + ROW_H / 2 + 4, label, 13, SOFT, KR, "end", 600)
    for c_i, (txt, c) in enumerate(cells):
        x = X0 + c_i * (COL_W + 24)
        if c is ACC: d.tone(x, y, COL_W, ROW_H, c, 8)
        else: d.box(x, y, COL_W, ROW_H, PAPER2, RULE, 1.0, 8)
        d.t(x + 16, y + 34, "가능" if c is OK else ("제한" if c is WARN else "헷갈림"), 13, c, KR, "start", 600)
        d.t(x + 16, y + 62, txt, 13, MUTED, KR, "start")

YB = Y0 + 2 * (ROW_H + 16) + 24
d.t(X0 - 152, YB, "완전히 idle 한 컨테이너에서 iostat 을 돌려도 CPU·디스크가 바쁘게 나옵니다 — 호스트 통계이기 때문입니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("호스트 통계가 새어 드는 자리", ACC), ("다 보이는 자리", OK), ("제한되는 자리", WARN)])
d.save("11-03.observability-inversion.svg")
