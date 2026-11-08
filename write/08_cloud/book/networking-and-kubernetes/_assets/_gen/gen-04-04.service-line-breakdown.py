# 04-04.service-line-breakdown — 서비스 하나가 노드마다 만드는 규칙 11줄의 구성
# 본문 요구: `## 서비스 하나의 규칙 줄` 의 확인된 것 — 11줄 = 진입 줄 1 + 서비스 체인 4줄(마킹 1 · 확률 2 · 나머지 1) + 엔드포인트 체인 셋의 6줄(각 2줄).
#           확률 값은 0.33333333349 → 0.50000000000 → 없음이고 ClusterIP 는 10.96.138.19 였다.
# 타입 스펙: type-tree — 부모 → 자식 분해. 왼쪽 뿌리 하나, 가운데 체인 셋, 오른쪽 잎 여덟. 줄 수는 노드 부제로 더해 보이고
#           coral focal 은 확률이 붙은 줄이 있는 서비스 체인 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 620


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "TREE · 04-04 SERVICE LINES",
      "서비스 하나의 11줄은 체인 셋에 나뉘어 있습니다",
      "default/web 서비스 하나가 노드마다 만드는 iptables 규칙 11줄의 분해. 진입 줄 1개, 서비스 체인 4줄(마킹 1, 확률 2, 나머지 1), "
      "엔드포인트 체인 셋의 6줄(체인마다 헤어핀 마킹과 DNAT 두 줄)을 더한 값이다. 확률은 0.33333333349, 0.50000000000, 없음 순이다.",
      lead="세 노드가 모두 같은 11줄을 갖습니다")

RX, RW = 24, 168
GX, GW = 250, 236
LX, LW = 560, 416
LH, STRIDE, Y0 = 46, 54, 112

LEAVES = [
    # (그룹, 제목, 부제)
    (0, "진입 줄", "10.96.138.19 · tcp · dport 80 → 서비스 체인"),
    (1, "마킹 줄", "패킷에 표시만 붙이고 다음 줄로"),
    (1, "확률 줄 1", "--probability 0.33333333349 → 엔드포인트 체인 1"),
    (1, "확률 줄 2", "--probability 0.50000000000 → 엔드포인트 체인 2"),
    (1, "나머지 줄", "확률 없음 → 엔드포인트 체인 3"),
    (2, "엔드포인트 체인 1", "2줄: 헤어핀 마킹 + DNAT"),
    (2, "엔드포인트 체인 2", "2줄: 헤어핀 마킹 + DNAT"),
    (2, "엔드포인트 체인 3", "2줄: 헤어핀 마킹 + DNAT"),
]
GROUPS = [
    ("진입 줄", "1줄", INFO),
    ("서비스 체인", "4줄 = 마킹 1 + 확률 2 + 나머지 1", ACC),
    ("엔드포인트 체인 셋", "6줄 = 3 × 2", INFO),
]

cy = [Y0 + i * STRIDE + LH / 2 for i in range(len(LEAVES))]
gcy = []
for g in range(3):
    rows = [cy[i] for i, l in enumerate(LEAVES) if l[0] == g]
    gcy.append(sum(rows) / len(rows))
rcy = sum(gcy) / 3

# 뿌리
d.box(RX, rcy - 36, RW, 72, PAPER2, RULE, 1.0, 8)
d.t(RX + RW / 2, rcy - 4, "default/web", 14, INK, MONO, "middle", 600)
d.t(RX + RW / 2, rcy + 18, "11줄 = 1 + 4 + 6", 12, MUTED, MONO, "middle")

# 뿌리 → 그룹: 줄기를 세워 한 점에서 갈라진다
sx = (RX + RW + GX) / 2
d.line(RX + RW, rcy, sx, rcy, SOFT, 1.3)
d.line(sx, min(gcy), sx, max(gcy), SOFT, 1.3)
for g in range(3):
    d.arrow([(sx, gcy[g]), (GX - 4, gcy[g])], SOFT, "soft", 1.3)

for g, (title, sub, c) in enumerate(GROUPS):
    y = gcy[g] - 32
    if c == ACC:
        d.tone(GX, y, GW, 64, ACC, 8, "1F", 1.6)
    else:
        d.tone(GX, y, GW, 64, c, 8, "14", 1.1)
    d.t(GX + GW / 2, y + 27, ddx.fit(title, 13, GW - 16, title), 13, c, kr(title), "middle", 600)
    d.t(GX + GW / 2, y + 48, ddx.fit(sub, 12, GW - 16, sub), 12, MUTED, kr(sub), "middle")

    # 그룹 → 잎
    rows = [cy[i] for i, l in enumerate(LEAVES) if l[0] == g]
    tx = (GX + GW + LX) / 2
    d.line(GX + GW, gcy[g], tx, gcy[g], SOFT, 1.3)
    if len(rows) > 1:
        d.line(tx, min(rows), tx, max(rows), SOFT, 1.3)
    for r in rows:
        d.arrow([(tx, r), (LX - 4, r)], SOFT, "soft", 1.3)

for i, (g, title, sub) in enumerate(LEAVES):
    y = Y0 + i * STRIDE
    d.box(LX, y, LW, LH, PAPER2, RULE, 0.9, 6)
    d.t(LX + 16, y + 19, ddx.fit(title, 12, LW - 32, title), 12, INK, kr(title), "start", 600)
    d.t(LX + 16, y + 37, ddx.fit(sub, 12, LW - 32, sub), 12, MUTED, kr(sub), "start")

d.legend(570, [("규칙 줄 묶음", INFO), ("확률이 붙은 체인", ACC)])
d.save("04-04.service-line-breakdown.svg")
print("ok service-line-breakdown")
