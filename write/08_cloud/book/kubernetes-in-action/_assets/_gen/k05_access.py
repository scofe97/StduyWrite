"""05-02 방법 ①~④ 공용 골격.

본문이 "각 방법의 홉 경로를 실제 쿠버네티스 아키텍처 위에 그린 그림을 함께 봅니다" 라고
못 박으므로 네 장은 같은 좌표계를 써야 한다. 계약의 "같은 종류를 여러 장 그리면 첫 장의
stride·여백을 나머지가 그대로 쓴다" 를 파일로 강제한다 — 눈대중으로 네 번 맞추지 않는다.

좌표를 잡을 때 두 가지가 걸렸고 여기서 한 번에 해결했다.
  · 노트북과 API 서버의 y 를 맞추지 않으면 그 홉이 비스듬해진다 → 둘 다 250 행에 둔다.
  · UPPER 와 POD 가 붙어 있으면 그 사이 연결선이 6px 로 뭉개진다 → 60px 을 띄운다.

홉 라벨은 번호 칩으로만 얹고 설명은 아래 산문이 맡는다. 상자 사이 통로가 좁아
문장 라벨을 넣으면 어느 장에서든 상자를 덮는다.
"""
from dd import INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 630
BAND = (104, 574)

LAPTOP = (100, 250, 152, 104)
CP_ZONE = (238, 182, 300, 268)
API = (388, 250, 250, 84)
ETC = (388, 388, 250, 64)
WK_ZONE = (586, 182, 374, 268)
UPPER = (773, 244, 290, 72)
POD = (773, 388, 290, 96)

DROP = f"M {UPPER[0]} {UPPER[1]+UPPER[3]//2+6} L {POD[0]} {POD[1]-POD[3]//2-10}"
DROP_CHIP = (UPPER[0], 308)
TO_API = f"M {LAPTOP[0]+LAPTOP[2]//2+6} {API[1]} L {API[0]-API[2]//2-8} {API[1]}"
TO_API_CHIP = (218, API[1])


def zone(d, rect, label, c, dim=False):
    x, y, w, h = rect
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{c}{"03" if dim else "06"}" stroke="{c}" stroke-width="1.2" '
               f'stroke-dasharray="7 6"{" opacity=\"0.45\"" if dim else ""}/>')
    ddx.ring_label(d, x, y, label, 11, SOFT if dim else c, off=16)


def slot(d, rect, title, sub, tag, c=None, dim=False):
    cx, cy, w, h = rect
    x, y = cx - w // 2, cy - h // 2
    if dim:
        d.box(x, y, w, h, PAPER, RULE, 0.8, 6); tc = SOFT
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - (18 if tag else 8), ddx.fit(title, 13, w - 18, title), 13, tc,
        MONO if all(ord(ch) < 128 for ch in title) else KR, "middle", 600)
    if sub:
        d.t(cx, cy + 4, ddx.fit(sub, 11, w - 16, title), 11, SOFT if dim else MUTED,
            MONO if all(ord(ch) < 128 or ch in ':.·' for ch in sub) else KR)
    if tag:
        d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, title), 10, SOFT, KR)


def hop(d, path, num, chip_xy):
    """굵은 앰버 경로 한 구간 + 번호 칩. 직각으로만 꺾는다."""
    d.path(path, ACC, 2.0, m="acc")
    d.chip(chip_xy[0], chip_xy[1], num, ACC, 11)


def verdict(d, hops, last, ip, note):
    d.line(36, 470, 964, 470, RULE, 0.8)
    d.t(36, 496, hops, 11, SOFT, KR, "start")
    d.t(36, 522, f"마지막으로 kiada 에게 연결을 연 것 = {last}", 12, MUTED, KR, "start")
    d.t(36, 548, "그래서 Client IP =", 12, MUTED, KR, "start")
    d.t(180, 548, ip, 13, ACC, MONO, "start", 600)
    d.t(190 + int(len(ip) * 8.5), 548, note, 11, SOFT, KR, "start")
