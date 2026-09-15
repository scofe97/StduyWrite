# 타입 스펙: type-architecture — 두 칸이 같은 망 조각(출발지 · 라우터 · 1500 링크 · 목적지)을 되풀이하고
#       칸마다 조각 하나가 닿는지만 바꾼다. 순서는 번호 배지로 보인다. gen-06-05.ecmp-flow-hash.py 와 같은 칸 반복 문법이다.
#       축약: 조각 막대 폭은 데이터 바이트 수에 비례한다(0.05 px/B 를 4 의 배수로 반올림). 헤더 20 B 칸은 비례가 아니다.
# 출처: 원문 §4.3.1 "Identifier, flags, fragmentation offset ... a large IP datagram is broken into several smaller
#       IP datagrams which are then forwarded independently to the destination, where they are reassembled".
#       절차는 원문이 다루지 않아("We'll not cover fragmentation here") 전부 RFC 에서 가져왔다.
#       - 식별자 16 비트 · 플래그 DF · MF · 오프셋 13 비트 8 바이트 단위: RFC 791 §3.1
#       - 첫 조각을 MTU 에 채우고 NFB = (MTU − IHL×4) / 8, 둘째 조각 오프셋 = 앞 오프셋 + NFB: RFC 791 §3.2 예시 절차
#       - 식별자 · 출발지 · 목적지 · 프로토콜이 같은 조각을 모아 오프셋 자리에 붙임: RFC 791 §2.3
#       - 재조립은 목적지에서만 · 타이머가 끝나면 모은 조각 전부 버림: RFC 791 §3.2
# 노트의 예시: 4,000 B 데이터그램(헤더 20 + 데이터 3,980) · DF 0 · 식별자 0x4d2a 는 고른 값이다.
#       조각 값(1,480 / 1,480 / 1,020 · 오프셋 0 / 185 / 370 · MF 1 / 1 / 0)은 위 절차로 계산했다.
#       어느 조각을 잃는지(둘째)는 예시다.
# focal: 둘째 칸의 사라진 조각 2 와 목적지의 빈칸 — 본문이 짚는 "하나를 잃으면 전체를 잃는다".
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 644
d = D(W, H, "IPV4 · FRAGMENTATION · RFC 791",
      "조각 셋이 다 와야 되붙고, 하나가 빠지면 전부 버립니다",
      "헤더 20 바이트와 데이터 3,980 바이트인 IPv4 데이터그램이 MTU 1500 링크 앞 라우터에서 조각 셋으로 갈린다. "
      "조각은 데이터 1,480 · 1,480 · 1,020 바이트, 오프셋 0 · 185 · 370, MF 1 · 1 · 0 이고 식별자는 셋이 같다. "
      "위 칸에서는 셋이 모두 목적지에 닿아 오프셋 자리에 맞춰 3,980 바이트로 되붙는다. "
      "아래 칸에서는 조각 2 가 도중에 사라져 목적지에 빈칸이 남고, 타이머가 끝나면 받은 조각까지 버린다.",
      "위는 조각 셋이 모두 닿을 때, 아래는 조각 2 가 사라질 때입니다. 쪼개는 방식은 두 칸이 같습니다")

PANEL_Y0, PANEL_H, PANEL_STRIDE = 96, 224, 240
ROW_DY = (76, 124, 172)                    # 조각 세 줄의 중심 y 오프셋 (stride 48)
SRC_X, SRC_W = 40, 96                      # 출발지
RT_X, RT_W = 400, 96                       # 라우터
DST_X, DST_W = 736, 232                    # 목적지
HDR_W, BAR_H = 16, 20                      # 헤더 칸 · 막대 높이
FRAG_X = 504                               # 조각이 링크 위에 놓이는 자리
CHIP_CX = 664

# 조각: (데이터 폭 px, 데이터 B, 오프셋, MF, 목적지 줄 위 시작 바이트)
FRAGS = [(76, "1,480", 0, 1, "0"), (76, "1,480", 185, 1, "1,480"), (52, "1,020", 370, 0, "2,960")]
ORIG_W = sum(f[0] for f in FRAGS)          # 204


def text_w(txt, size):
    return sum(size if "가" <= ch <= "힣" else size * 0.6 for ch in txt)


def badge(cx, cy, n, c):
    d.box(cx - 10, cy - 10, 20, 20, PAPER, c, 1.2, 4)
    d.t(cx, cy + 5, str(n), 12, c, MONO, "middle", 600)


def step(x, y, n, label, c=MUTED, label_c=None):
    badge(x, y, n, c)
    d.t(x + 16, y + 5, label, 13, label_c or c, KR, "start", 600)


def cross(x, y, c):
    d.line(x - 7, y - 7, x + 7, y + 7, c, 2.0)
    d.line(x - 7, y + 7, x + 7, y - 7, c, 2.0)


def datagram(x, cy, data_w, label, c=INFO, lost=False):
    """헤더 칸 + 데이터 막대. lost 면 점선 테두리만 남긴다."""
    top = cy - BAR_H / 2
    d.box(x, top, HDR_W + data_w, BAR_H, PAPER, "none", 0, 3)          # 링크 선이 비치지 않게
    if lost:
        d.path(f"M {x} {top} L {x + HDR_W + data_w} {top} L {x + HDR_W + data_w} {top + BAR_H} "
               f"L {x} {top + BAR_H} L {x} {top}", c, 1.4, dash="4 3")
    else:
        d.tone(x, top, HDR_W, BAR_H, c, 2, "33", 1.1)
        d.tone(x + HDR_W, top, data_w, BAR_H, c, 2, "18", 1.1)
    d.t(x + HDR_W / 2, cy + 4, "H", 11, c, MONO, "middle", 600)
    d.t(x + HDR_W + data_w / 2, cy + 5, label, 12, c, MONO, "middle", 600)


def field_chip(cy, txt, c=INFO):
    w = text_w(txt, 12) + 12
    d.box(CHIP_CX - w / 2, cy - 10, w, 20, PAPER, c, 0.9, 4)
    d.t(CHIP_CX, cy + 4, txt, 12, c, KR, "middle")


def panel(i, title, lost_row=None):
    y0 = PANEL_Y0 + i * PANEL_STRIDE
    if lost_row is None:
        d.box(24, y0, 952, PANEL_H, f"{INK}05", RULE, 1.0, 10)
    else:
        d.tone(24, y0, 952, PANEL_H, ACC, 10, "0A", 1.4)
    d.t(40, y0 + 24, title, 13, INK, KR, "start", 600)
    rows = [y0 + dy for dy in ROW_DY]
    mid = rows[1]

    # 1 · 출발지 → 라우터 · 원본 데이터그램
    d.arrow([(SRC_X + SRC_W, mid), (RT_X - 4, mid)], MUTED, "ar", 1.4)
    datagram(156, mid, ORIG_W, "3,980")
    step(164, mid - 32, 1, "원본 4,000 B · DF 0")
    d.box(SRC_X, mid - 28, SRC_W, 56, PAPER2, RULE, 1.0, 6)
    d.t(SRC_X + SRC_W / 2, mid - 4, "출발지", 13, INK, KR, "middle", 600)
    d.t(SRC_X + SRC_W / 2, mid + 16, "호스트", 12, MUTED, KR)

    # 2 · 라우터가 쪼갬
    top, bot = rows[0] - 28, rows[2] + 28
    for k, cy in enumerate(rows):
        if k == lost_row:
            d.path(f"M {RT_X + RT_W} {cy} L 700 {cy}", ACC, 1.4, dash="5 4")
            cross(708, cy, ACC)
        else:
            d.arrow([(RT_X + RT_W, cy), (DST_X, cy)], MUTED, "ar", 1.4)
    d.box(RT_X, top, RT_W, bot - top, PAPER2, MUTED, 1.2, 6)
    badge(RT_X + 28, top + 20, 2, MUTED)
    d.t(RT_X + 44, top + 25, "쪼갬", 13, MUTED, KR, "start", 600)
    d.t(RT_X + RT_W / 2, top + 64, "라우터", 13, INK, KR, "middle", 600)
    d.t(RT_X + RT_W / 2, top + 92, "다음 링크", 12, MUTED, KR)
    d.t(RT_X + RT_W / 2, top + 112, "MTU 1500", 12, INFO, MONO)

    # 3 · 조각마다 따로 전달
    for k, (fw, fb, off, mf, _) in enumerate(FRAGS):
        cy = rows[k]
        datagram(FRAG_X, cy, fw, fb, ACC if k == lost_row else INFO, lost=(k == lost_row))
        if k != lost_row:
            field_chip(cy, f"오프셋 {off} · MF {mf}")
    if lost_row is None:
        step(FRAG_X + 8, y0 + 44, 3, "조각마다 따로 전달")
    else:
        step(FRAG_X + 8, y0 + 44, 3, f"조각 {lost_row + 1} 사라짐", ACC)
    d.t(FRAG_X, y0 + 212, "식별자 0x4d2a · 셋 다 같음", 12, SOFT, KR, "start")

    # 4 · 목적지에서만 되붙임
    d.box(DST_X, top, DST_W, y0 + 216 - top, PAPER2, RULE, 1.0, 6)
    d.t(DST_X + DST_W / 2, top + 22, "목적지", 13, INK, KR, "middle", 600)
    d.t(DST_X + DST_W / 2, top + 42, "재조립은 여기서만", 12, MUTED, KR)
    sx, sy = DST_X + 8, y0 + 112
    c_done = OK if lost_row is None else INFO
    d.tone(sx, sy, HDR_W, 24, c_done, 2, "33", 1.1)
    d.t(sx + HDR_W / 2, sy + 16, "H", 11, c_done, MONO, "middle", 600)
    for k, (fw, _, _, _, start) in enumerate(FRAGS):
        x = sx + HDR_W + sum(f[0] for f in FRAGS[:k])
        if k == lost_row:
            d.path(f"M {x} {sy} L {x + fw} {sy} L {x + fw} {sy + 24} L {x} {sy + 24} L {x} {sy}", ACC, 1.6, dash="4 3")
            d.t(x + fw / 2, sy + 17, "빈칸", 12, ACC, KR, "middle", 600)
        else:
            d.tone(x, sy, fw, 24, c_done, 2, "22", 1.1)
        d.t(x + 2, sy + 42, start, 11, SOFT, MONO, "start")
    if lost_row is None:
        step(DST_X + 20, y0 + 180, 4, "오프셋 자리에 붙임", MUTED)
        d.t(DST_X + 36, y0 + 206, "데이터 3,980 B 복원", 13, OK, KR, "start", 600)
    else:
        step(DST_X + 20, y0 + 180, 4, "빈칸 · 못 맞춤", ACC)
        step(DST_X + 20, y0 + 206, 5, "타이머 끝 · 전부 버림", BAD)


panel(0, "1. 조각 셋이 모두 닿을 때")
panel(1, "2. 조각 하나가 사라질 때", lost_row=1)

d.legend(584, [("데이터그램 · 조각", INFO), ("되붙은 데이터", OK), ("모은 조각 버림", BAD), ("사라진 조각 · 본문이 짚는 곳", ACC)])
d.t(960, 636, "RFC 791 §2.3 · §3.1 · §3.2", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.fragmentation.svg"
d.save(out)
print("→", out)
