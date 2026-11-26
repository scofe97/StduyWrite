# 타입 스펙: type-timeline
# 01-01 Recreate 소절 — v1 Pod 4개 전원 종료 -> Pod 0개 다운타임 구간 -> v2 Pod 4개 기동·Ready 시간축
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
LEGEND_Y = 412
H = LEGEND_Y + 44  # 456 (margin = 456 - 436 = 20 >= 16)

d = D(
    W,
    H,
    "TIMELINE · RECREATE DOWNTIME",
    "Recreate 배포의 Pod 교체와 다운타임 구간",
    "replicas 4 기준, v1 Pod 4개 전원 종료 후 Pod 0개 구간에서 Ingress 503과 ClusterIP 연결 거부가 발생하고, v2 Pod 4개 기동·Ready 후 서비스가 재개되는 시간축",
    lead="replicas: 4 기준 — v1 전원 종료 뒤에야 v2 를 생성하므로 가용 Pod 0개 구간에 서비스가 중단됩니다",
)

# 시간축 경계 x 좌표 (전부 4의 배수, 구간 길이는 단계 비중을 반영)
X0, X1, X2, X3, X4 = 104, 276, 460, 724, 908
AXIS_Y = 264
TOP_Y, TOP_H = 104, 124
BOT_Y, BOT_H = 336, 52

# 행 라벨 (좌측 열)
d.t(16, TOP_Y + TOP_H // 2 + 4, "Pod 상태", 13, MUTED, KR, "start", 600)
d.t(16, AXIS_Y + 4, "시간축", 13, MUTED, KR, "start", 600)
d.t(16, BOT_Y + BOT_H // 2 + 4, "요청 결과", 13, MUTED, KR, "start", 600)

# ── 1. 시간축 기준선과 경계선 (z-order: 카드·원보다 먼저) ──────────────────
for tx in (X0, X1, X2, X3, X4):
    d.line(tx, TOP_Y + TOP_H, tx, AXIS_Y - 6, RULE, 1.0, dash="3 3")
    d.line(tx, AXIS_Y + 6, tx, AXIS_Y + 14, RULE, 1.0)

d.arrow([(X0, AXIS_Y), (944, AXIS_Y)], c=MUTED, m="ar", sw=1.2)

# ── 2. 상단 구간: Pod 상태 (t0~t4) ────────────────────────────────────────
# Phase 1: v1 운영 (4개 Ready)
p1_x, p1_w = X0 + 4, (X1 - X0) - 8  # 108, 164
d.box(p1_x, TOP_Y, p1_w, TOP_H, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(p1_x + p1_w // 2, TOP_Y + 22, "v1 운영", 13, INK, KR, "middle", 600)
for i in range(4):
    col_i, row_i = i % 2, i // 2
    px = p1_x + 14 + col_i * 72
    py = TOP_Y + 36 + row_i * 30
    d.tone(px, py, 64, 24, INFO, r=4, op="18", sw=1.1)
    d.t(px + 32, py + 16, "v1", 12, INFO, MONO, "middle", 600)
d.t(p1_x + p1_w // 2, TOP_Y + 112, "Ready 4 / 4", 11, INFO, MONO, "middle", 600)

# Phase 2: v1 4개 종료
p2_x, p2_w = X1 + 4, (X2 - X1) - 8  # 280, 176
d.box(p2_x, TOP_Y, p2_w, TOP_H, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(p2_x + p2_w // 2, TOP_Y + 22, "v1 4개 종료", 13, WARN, KR, "middle", 600)
for i in range(4):
    col_i, row_i = i % 2, i // 2
    px = p2_x + 16 + col_i * 76
    py = TOP_Y + 36 + row_i * 30
    d.o.append(
        f'<rect x="{px}" y="{py}" width="68" height="24" rx="4" '
        f'fill="{WARN}12" stroke="{WARN}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    )
    d.t(px + 34, py + 16, "v1", 12, WARN, MONO, "middle", 600, op="0.85")
d.t(p2_x + p2_w // 2, TOP_Y + 112, "Terminating 4→0", 11, WARN, MONO, "middle", 600)

# Phase 3: Pod 0개 구간 (FOCAL 1곳)
p3_x, p3_w = X2 + 4, (X3 - X2) - 8  # 464, 256
d.tone(p3_x, TOP_Y, p3_w, TOP_H, ACC, r=6, op="12", sw=1.4)
d.t(p3_x + p3_w // 2, TOP_Y + 22, "Pod 0개 구간", 13, ACC, KR, "middle", 600)
d.o.append(
    f'<rect x="{p3_x + 24}" y="{TOP_Y + 36}" width="{p3_w - 48}" height="54" rx="4" '
    f'fill="{PAPER}" stroke="{ACC}" stroke-width="1.1" stroke-dasharray="5 3"/>'
)
d.t(p3_x + p3_w // 2, TOP_Y + 58, "가용 Pod 0개", 14, ACC, KR, "middle", 600)
d.t(p3_x + p3_w // 2, TOP_Y + 80, "v1 0 · v2 기동 중", 13, MUTED, KR, "middle", 400)
d.t(p3_x + p3_w // 2, TOP_Y + 112, "Ready 0 / 4", 11, ACC, MONO, "middle", 600)

# Phase 4: v2 4개 기동 · Ready
p4_x, p4_w = X3 + 4, (X4 - X3) - 8  # 728, 176
d.box(p4_x, TOP_Y, p4_w, TOP_H, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(p4_x + p4_w // 2, TOP_Y + 22, "v2 4개 기동 · Ready", 13, OK, KR, "middle", 600)
for i in range(4):
    col_i, row_i = i % 2, i // 2
    px = p4_x + 16 + col_i * 76
    py = TOP_Y + 36 + row_i * 30
    d.tone(px, py, 68, 24, OK, r=4, op="18", sw=1.1)
    d.t(px + 34, py + 16, "v2", 12, OK, MONO, "middle", 600)
d.t(p4_x + p4_w // 2, TOP_Y + 112, "Ready 4 / 4", 11, OK, MONO, "middle", 600)

# ── 3. 시간축 마일스톤 원 · 눈금 라벨 ────────────────────────────────────
milestones = [
    (X0, 4, INFO, "t0", None),
    (X1, 4, WARN, "t1", "배포 시작"),
    (X2, 6, ACC, "t2", "종료 완료"),
    (X3, 4, OK, "t3", "v2 Ready"),
    (X4, 4, OK, "t4", None),
]
for tx, rad, col, tlab, sub in milestones:
    d.o.append(
        f'<circle cx="{tx}" cy="{AXIS_Y}" r="{rad}" fill="{col}" stroke="{PAPER}" stroke-width="1.5"/>'
    )
    d.t(tx, AXIS_Y + 28, tlab, 11, col if rad == 6 else MUTED, MONO, "middle", 600)
    if sub:
        sfam = KR if any("가" <= ch <= "힣" for ch in sub) else MONO
        ssize = 13 if sfam == KR else 11
        d.t(tx, AXIS_Y + 46, sub, ssize, col, sfam, "middle", 600)

# ── 4. 하단 구간: 요청 결과 (다운타임 띠) ─────────────────────────────────
ribbons = [
    (X0 + 4, (X1 - X0) - 8, INFO, "14", 1.1, "요청 정상", "v1 100%", INFO, MUTED),
    (X1 + 4, (X2 - X1) - 8, WARN, "14", 1.1, "엔드포인트 제거", "연결 드레인", WARN, MUTED),
    (X2 + 4, (X3 - X2) - 8, BAD, "18", 1.4, "다운타임 · 요청 실패", "Ingress 503 · ClusterIP 거부", BAD, INK),
    (X3 + 4, (X4 - X3) - 8, OK, "14", 1.1, "요청 정상", "v2 100%", OK, MUTED),
]
for rx, rw, col, op, sw, line1, line2, c1, c2 in ribbons:
    d.tone(rx, BOT_Y, rw, BOT_H, col, r=6, op=op, sw=sw)
    cx = rx + rw // 2
    d.t(cx, BOT_Y + 22, line1, 13, c1, KR, "middle", 600)
    f2 = KR if any("가" <= ch <= "힣" for ch in line2) else MONO
    s2 = 13 if f2 == KR else 11
    d.t(cx, BOT_Y + 42, line2, s2, c2, f2, "middle", 400)

# ── 5. 범례 ───────────────────────────────────────────────────────────────
d.legend(
    LEGEND_Y,
    [
        ("v1 운영", INFO),
        ("v1 종료", WARN),
        ("Pod 0 구간", ACC),
        ("다운타임 · 실패", BAD),
        ("v2 Ready", OK),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "01-01.recreate-downtime.svg")
)
d.save(out_path)
print(f"saved: {out_path}")
