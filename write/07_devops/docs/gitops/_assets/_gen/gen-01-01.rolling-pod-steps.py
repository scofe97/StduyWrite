# 타입 스펙: type-process
# 01-01 RollingUpdate 소절 — replicas 4 · maxSurge 1 · maxUnavailable 0 기준 t0~t4 단계별 Pod 교체 흐름
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W = 1000
MARGIN_X = 20
BOX_W = 128
GAP = 80
STRIDE = BOX_W + GAP  # 208

CARD_Y = 144
CARD_H = 264
POD_W = 104
POD_H = 28
POD_STRIDE = 36
POD_Y0 = CARD_Y + 12  # 156
DIV_Y = 340
AY = 244

LEGEND_Y = 432
H = LEGEND_Y + 44  # 476 (margin = 476 - 456 = 20 >= 16)

d = D(
    W,
    H,
    "PROCESS · ROLLINGUPDATE POD STEPS",
    "RollingUpdate 단계별 Pod 교체 흐름",
    "replicas 4, maxSurge 1, maxUnavailable 0 설정에서 t0부터 t4까지 새 v2 Pod가 readiness를 통과할 때마다 v1이 4에서 0으로, v2가 0에서 4로 교체되는 과정",
    lead="replicas: 4 · maxSurge: 1 · maxUnavailable: 0 기준 — 새 Pod 가 readiness 통과 뒤에야 기존 Pod 를 종료합니다",
)

# (step_id, step_label, pods, count_label, svc_ratio, is_focal)
# pod tuple: ("v1" | "v2" | "v2_wait")
stages = [
    (
        "t0",
        "초기",
        ["v1", "v1", "v1", "v1"],
        "v1 4 · v2 0",
        "Service 100/0",
        False,
    ),
    (
        "t1",
        "기동 +1",
        ["v1", "v1", "v1", "v1", "v2_wait"],
        "v1 4 · v2 +1",
        "Service 100/0",
        True,
    ),
    (
        "t2",
        "교체 1",
        ["v1", "v1", "v1", "v2", "v2_wait"],
        "v1 3 · v2 1+1",
        "Service 75/25",
        False,
    ),
    (
        "t3",
        "교체 3",
        ["v1", "v2", "v2", "v2", "v2_wait"],
        "v1 1 · v2 3+1",
        "Service 25/75",
        False,
    ),
    (
        "t4",
        "완료",
        ["v2", "v2", "v2", "v2"],
        "v1 0 · v2 4",
        "Service 0/100",
        False,
    ),
]

# (top_mono, bot_kr, color, marker)
transitions = [
    ("maxSurge", "+1 기동", ACC, "acc"),
    ("readiness", "통과", ACC, "acc"),
    ("readiness", "2회 반복", OK, "ok"),
    ("readiness", "통과", OK, "ok"),
]

# ── 1. 단계 간 화살표 (z-order: 카드보다 먼저) ────────────────────────────
for idx, (top_txt, bot_txt, col, mk) in enumerate(transitions):
    x_start = MARGIN_X + idx * STRIDE + BOX_W
    x_end = MARGIN_X + (idx + 1) * STRIDE - 2
    mx = (x_start + x_end) // 2
    d.arrow([(x_start, AY), (x_end, AY)], c=col, m=mk, sw=1.4)
    d.t(mx, AY - 12, top_txt, 11, col, MONO, "middle", 600)
    d.t(mx, AY + 24, bot_txt, 13, col, KR, "middle", 600)

# ── 2. 단계 헤더 · 카드 · Pod 상자 ────────────────────────────────────────
for idx, (sid, slabel, pods, cnt_txt, svc_txt, focal) in enumerate(stages):
    x0 = MARGIN_X + idx * STRIDE
    cx = x0 + BOX_W // 2

    # 단계 번호 pill
    pw, ph = 36, 20
    px_pill = cx - pw // 2
    if focal:
        d.o.append(
            f'<rect x="{px_pill}" y="92" width="{pw}" height="{ph}" rx="10" '
            f'fill="{ACC}22" stroke="{ACC}" stroke-width="1.2"/>'
        )
        d.t(cx, 106, sid, 11, ACC, MONO, "middle", 600)
        d.t(cx, 132, slabel, 13, ACC, KR, "middle", 600)
        d.tone(x0, CARD_Y, BOX_W, CARD_H, ACC, r=6, op="12", sw=1.4)
    else:
        d.o.append(
            f'<rect x="{px_pill}" y="92" width="{pw}" height="{ph}" rx="10" '
            f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>'
        )
        d.t(cx, 106, sid, 11, INK, MONO, "middle", 600)
        d.t(cx, 132, slabel, 13, MUTED, KR, "middle", 600)
        d.box(x0, CARD_Y, BOX_W, CARD_H, fill=PAPER2, stroke=RULE, sw=1.0, r=6)

    # Pod 상자 4~5개 (위에서 아래로)
    pod_x = cx - POD_W // 2
    for slot, kind in enumerate(pods):
        py = POD_Y0 + slot * POD_STRIDE
        if kind == "v1":
            d.tone(pod_x, py, POD_W, POD_H, INFO, r=4, op="18", sw=1.1)
            d.t(cx, py + 19, "v1", 12, INFO, MONO, "middle", 600)
        elif kind == "v2":
            d.tone(pod_x, py, POD_W, POD_H, OK, r=4, op="18", sw=1.1)
            d.t(cx, py + 19, "v2", 12, OK, MONO, "middle", 600)
        else:
            d.o.append(
                f'<rect x="{pod_x}" y="{py}" width="{POD_W}" height="{POD_H}" rx="4" '
                f'fill="{WARN}14" stroke="{WARN}" stroke-width="1.3" stroke-dasharray="5 3"/>'
            )
            d.t(cx, py + 19, "v2 미준비", 13, WARN, KR, "middle", 600)

    # 카드 하단 요약 (Pod 수 + Service 트래픽 비율)
    d.line(x0 + 12, DIV_Y, x0 + BOX_W - 12, DIV_Y, RULE, 0.8)
    d.t(cx, 364, cnt_txt, 11, INK, MONO, "middle", 600)
    svc_col = OK if idx == 4 else (INFO if idx <= 1 else MUTED)
    d.t(cx, 388, svc_txt, 11, svc_col, MONO, "middle", 600)

# ── 3. 범례 ───────────────────────────────────────────────────────────────
d.legend(
    LEGEND_Y,
    [
        ("v1 Ready", INFO),
        ("v2 Ready", OK),
        ("v2 미준비 (점선)", WARN),
        ("maxSurge +1 단계", ACC),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "01-01.rolling-pod-steps.svg")
)
d.save(out_path)
print(f"saved: {out_path}")
