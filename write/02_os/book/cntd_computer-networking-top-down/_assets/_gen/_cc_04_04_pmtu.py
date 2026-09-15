# 04-04 §1 경로 MTU 세 장의 공용 골격 — 송신자 · 방화벽 · 터널 입구 라우터 · 수신자를 가로 한 줄에 두고
# 위 한 줄 · 아래 세 줄의 트랙에 번호 붙은 수평 화살표로 순서를 보인다.
# 세 장(문제 · 경로 MTU 발견 · MSS 클램핑)이 같은 노드 자리와 트랙 stride 를 쓰도록 좌표를 여기 한 곳에 둔다.
# 달라지는 것은 방화벽 · 라우터의 설명 한 줄과 트랙 위에 무엇이 지나가는지뿐이고, 그 차이가 세 장의 논점이다.
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 528
NODE_Y, NODE_H = 176, 64
NODE_CY = NODE_Y + NODE_H // 2              # 208
SND_X, FW_X, RT_X, RCV_X = 40, 264, 488, 840
SND_W, FW_W, RT_W, RCV_W = 120, 120, 136, 120
SND_CX, FW_CX, RT_CX, RCV_CX = 100, 324, 556, 900
UP = 136                                     # 노드 위 트랙
DN = (288, 344, 400)                         # 노드 아래 트랙 (stride 56)
CHIP_Y = 436
LEGEND_Y = 468
DROP_X = RT_X + 16                           # 라우터 앞에서 버려지는 자리


def frame(eyebrow, title, desc, lead):
    return D(W, H, eyebrow, title, desc, lead)


def _node(d, x, w, name, sub, sub_c=MUTED, stroke=RULE):
    d.box(x, NODE_Y, w, NODE_H, PAPER2, stroke, 1.0, 7)
    d.t(x + w / 2, NODE_Y + 26, name, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, NODE_Y + 48, sub, 12, sub_c, KR)


def _link_chip(d, cx, txt, c=MUTED):
    w = len(txt) * 7.2 + 12
    d.box(cx - w / 2, NODE_CY - 10, w, 20, PAPER, c, 0.8, 4)
    d.t(cx, NODE_CY + 4, txt, 12, c, MONO)


def topology(d, fw_sub, fw_c, rt_sub, rt_c=MUTED):
    """노드 넷과 링크 셋. 링크 선을 먼저 그려 상자가 선 끝을 덮게 한다."""
    d.line(SND_X + SND_W, NODE_CY, FW_X, NODE_CY, MUTED, 1.4)
    d.line(FW_X + FW_W, NODE_CY, RT_X, NODE_CY, MUTED, 1.4)
    d.tone(RT_X + RT_W, NODE_CY - 12, RCV_X - RT_X - RT_W, 24, INFO, 4, "14", 1.1)
    d.t((RT_X + RT_W + RCV_X) / 2, NODE_CY + 5, "터널 안쪽 1480", 12, INFO, KR, "middle", 600)
    _link_chip(d, (SND_X + SND_W + FW_X) / 2, "1500")
    _link_chip(d, (FW_X + FW_W + RT_X) / 2, "1500")
    _node(d, SND_X, SND_W, "송신자", "IPv6 호스트")
    _node(d, FW_X, FW_W, "방화벽", fw_sub, fw_c)
    _node(d, RT_X, RT_W, "터널 입구 라우터", rt_sub, rt_c)
    _node(d, RCV_X, RCV_W, "수신자", "터널 건너편")


def badge(d, cx, cy, n, c):
    d.box(cx - 10, cy - 10, 20, 20, PAPER, c, 1.2, 4)
    d.t(cx, cy + 5, str(n), 12, c, MONO, "middle", 600)


def step(d, x, track_y, n, label, c):
    """트랙 위 번호 배지와 라벨. 배지는 트랙 20px 위에 둔다."""
    badge(d, x, track_y - 20, n, c)
    fam = KR if any("가" <= ch <= "힣" for ch in label) else MONO
    d.t(x + 16, track_y - 15, label, 13, c, fam, "start", 600)


def cross(d, x, y, c):
    d.line(x - 7, y - 7, x + 7, y + 7, c, 2.0)
    d.line(x - 7, y + 7, x + 7, y - 7, c, 2.0)


def send(d, y, x1, x2, c, dash=None, drop=None):
    """수평 화살표 한 줄. drop 이 색이면 화살촉 대신 그 색의 X 로 끝낸다."""
    m = {OK: "ok", INFO: "info", ACC: "acc", BAD: "bad"}.get(c, "ar")
    if drop is None:
        d.arrow([(x1, y), (x2, y)], c, m, 1.7, dash)
    else:
        step_back = -12 if x2 > x1 else 12
        d.path(f"M {x1} {y} L {x2 + step_back} {y}", c, 1.7, dash=dash)
        cross(d, x2, y, drop)


def chip(d, cx, cy, txt, c):
    w = sum(13 if "가" <= ch <= "힣" else 7.8 for ch in txt) + 20
    d.tone(cx - w / 2, cy - 12, w, 24, c, 4, "18", 1.1)
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)
