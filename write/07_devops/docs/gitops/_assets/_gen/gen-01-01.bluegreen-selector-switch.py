# 타입 스펙: type-architecture
# 01-01 §2 Blue-Green — Service selector(version: blue -> green) 전환과 즉시 롤백 점선 흐름.
# 본문 근거: 01-01.배포 전략 비교 L114-L149 (Blue-Green 소절) + handoff 3 Pod 규모 지정.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO  # noqa: E402

W = 960
PANEL_Y = 96
PANEL_H = 248
PANEL_W = 404
LEFT_X = 16
RIGHT_X = 540
MID_X = 480

LEGEND_Y = PANEL_Y + PANEL_H + 24  # 368
H = LEGEND_Y + 44  # 412 (margin = 412 - (368 + 24) = 20 >= 16)

d = D(
    W,
    H,
    "ARCHITECTURE · BLUE-GREEN SELECTOR SWITCH",
    "Blue-Green 배포의 Service 선택자 전환과 즉시 롤백",
    "전환 전에는 Ingress 에서 Service(my-api, version: blue) 가 Blue Deployment(v1, 3 Pod) 로 100% 트래픽을 보내고 "
    "Green Deployment(v2, 3 Pod) 를 미리 띄워 둔다. kubectl patch 로 selector 를 version: green 으로 바꾸면 "
    "트래픽 100% 가 Green 으로 일괄 이동하고, 장애 시 selector 를 version: blue 로 되돌리는 점선으로 즉시 복구한다.",
    lead="Green(v2, 3 Pod) 을 미리 띄운 뒤 kubectl patch 로 Service selector 만 바꿔 100% 를 일괄 전환합니다",
)


def draw_pods(bx, by, n, fill_c, stroke_c, active=True):
    """Deployment 상자 하단에 Pod 3개를 도형 개수로 표현한다."""
    pw, ph, gap = 30, 14, 8
    total_w = n * pw + (n - 1) * gap  # 106
    sx = bx + (132 - total_w) // 2  # bx + 13
    py = by + 56
    dash = "" if active else ' stroke-dasharray="3 2"'
    fill = f"{fill_c}44" if active else f"{fill_c}18"
    for i in range(n):
        px = sx + i * (pw + gap)
        d.o.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="3" '
            f'fill="{fill}" stroke="{stroke_c}" stroke-width="1.0"{dash}/>'
        )


def draw_panel(x0, header, is_after):
    # 1. Zone container
    d.o.append(
        f'<rect x="{x0}" y="{PANEL_Y}" width="{PANEL_W}" height="{PANEL_H}" rx="8" '
        f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>'
    )
    d.t(x0 + 14, PANEL_Y + 18, header, 9, SOFT, MONO, "start", 600)

    # Coordinates inside panel (all multiples of 4)
    ing_x, ing_y, ing_w, ing_h = x0 + 12, 196, 68, 64  # mid_y = 228
    svc_x, svc_y, svc_w, svc_h = x0 + 112, 192, 116, 72  # mid_y = 228
    dep_x, dep_w, dep_h = x0 + 260, 132, 84
    blue_y = 132   # mid_y = 174
    green_y = 240  # mid_y = 282
    bend_x = x0 + 244

    # 2. Connectors (z-order: before boxes)
    active_col = OK if is_after else INFO
    active_mk = "ok" if is_after else "info"

    # Ingress -> Service (32px)
    d.arrow([(ing_x + ing_w, 228), (svc_x, 228)], c=active_col, m=active_mk, sw=1.6)
    d.t((ing_x + ing_w + svc_x) // 2, 216, "100%", 11, active_col, MONO, "middle", 600)

    # Service -> Active Deployment (orthogonal 2-bend)
    if not is_after:
        d.arrow(
            [(svc_x + svc_w, 212), (bend_x, 212), (bend_x, 174), (dep_x, 174)],
            c=INFO,
            m="info",
            sw=1.6,
        )
    else:
        d.arrow(
            [(svc_x + svc_w, 244), (bend_x, 244), (bend_x, 282), (dep_x, 282)],
            c=OK,
            m="ok",
            sw=1.6,
        )

    # 3. Component boxes
    # Ingress
    d.box(ing_x, ing_y, ing_w, ing_h, fill=PAPER, stroke=RULE, sw=1.0, r=6)
    d.t(ing_x + ing_w // 2, ing_y + 26, "Ingress", 12, INK, MONO, "middle", 600)
    d.t(ing_x + ing_w // 2, ing_y + 46, "트래픽", 13, MUTED, KR, "middle")

    # Service (focal ACC in AFTER panel)
    if is_after:
        d.tone(svc_x, svc_y, svc_w, svc_h, ACC, r=6, op="12", sw=1.4)
        sel_txt, sel_col = "version: green", ACC
    else:
        d.tone(svc_x, svc_y, svc_w, svc_h, INFO, r=6, op="12", sw=1.2)
        sel_txt, sel_col = "version: blue", INFO
    d.t(svc_x + svc_w // 2, svc_y + 22, "Service", 13, INK, MONO, "middle", 600)
    d.t(svc_x + svc_w // 2, svc_y + 39, "my-api", 11, MUTED, MONO, "middle")
    d.t(svc_x + svc_w // 2, svc_y + 58, sel_txt, 11, sel_col, MONO, "middle", 600)

    # Blue Deployment (v1, 3 Pod)
    if not is_after:
        d.tone(dep_x, blue_y, dep_w, dep_h, INFO, r=6, op="14", sw=1.2)
        d.t(dep_x + dep_w // 2, blue_y + 22, "Blue · v1", 13, INFO, MONO, "middle", 600)
        d.t(dep_x + dep_w // 2, blue_y + 42, "100% · 3 Pod", 11, INK, MONO, "middle", 600)
        draw_pods(dep_x, blue_y, 3, INFO, INFO, active=True)
    else:
        d.o.append(
            f'<rect x="{dep_x}" y="{blue_y}" width="{dep_w}" height="{dep_h}" rx="6" '
            f'fill="{PAPER}" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="4 3"/>'
        )
        d.t(dep_x + dep_w // 2, blue_y + 22, "Blue · v1", 13, MUTED, MONO, "middle", 600)
        d.t(dep_x + dep_w // 2, blue_y + 42, "0% · 3 Pod 대기", 13, MUTED, KR, "middle")
        draw_pods(dep_x, blue_y, 3, MUTED, MUTED, active=False)

    # Green Deployment (v2, 3 Pod)
    if not is_after:
        d.o.append(
            f'<rect x="{dep_x}" y="{green_y}" width="{dep_w}" height="{dep_h}" rx="6" '
            f'fill="{PAPER}" stroke="{OK}" stroke-width="1.0" stroke-dasharray="4 3"/>'
        )
        d.t(dep_x + dep_w // 2, green_y + 22, "Green · v2", 13, OK, MONO, "middle", 600)
        d.t(dep_x + dep_w // 2, green_y + 42, "0% · 3 Pod 대기", 13, MUTED, KR, "middle")
        draw_pods(dep_x, green_y, 3, OK, OK, active=False)
    else:
        d.tone(dep_x, green_y, dep_w, dep_h, OK, r=6, op="14", sw=1.2)
        d.t(dep_x + dep_w // 2, green_y + 22, "Green · v2", 13, OK, MONO, "middle", 600)
        d.t(dep_x + dep_w // 2, green_y + 42, "100% · 3 Pod", 11, INK, MONO, "middle", 600)
        draw_pods(dep_x, green_y, 3, OK, OK, active=True)


# Middle transition arrows (BEFORE <-> AFTER)
# Forward switch: kubectl patch (version: green)
d.arrow([(LEFT_X + PANEL_W + 4, 188), (RIGHT_X - 4, 188)], c=ACC, m="acc", sw=1.8)
d.t(MID_X, 174, "kubectl patch", 11, ACC, MONO, "middle", 600)
d.t(MID_X, 208, "version: green", 11, ACC, MONO, "middle", 600)

# Rollback dashed arrow: version: blue
d.arrow([(RIGHT_X - 4, 276), (LEFT_X + PANEL_W + 4, 276)], c=WARN, m="warn", sw=1.5, dash="5 4")
d.t(MID_X, 262, "롤백 patch", 13, WARN, KR, "middle", 600)
d.t(MID_X, 296, "version: blue", 11, WARN, MONO, "middle", 600)

# Draw both panels
draw_panel(LEFT_X, "BEFORE", is_after=False)
draw_panel(RIGHT_X, "AFTER", is_after=True)

# Legend
d.legend(
    LEGEND_Y,
    [
        ("Blue · v1", INFO),
        ("Green · v2", OK),
        ("selector 전환", ACC),
        ("롤백 점선", WARN),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "01-01.bluegreen-selector-switch.svg")
)
d.save(out_path)
print(f"ok {pathlib.Path(out_path).name}")
