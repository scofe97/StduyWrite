# 05-03 실습 편 — 한 단계의 캡처를 시간순 메시지로 그리는 공용 틀.
# 타입 스펙: type-sequence — 컨테이너 레인 셋, 위에서 아래로 시간. 레인 중심은 모든 장이 같은 stride 280 을 쓴다.
# 선 규약: 실선 = 캡처 지점에 찍힌 프레임, 점선 = 선 위에는 있었으나 이 캡처에는 없는 프레임(로그·다른 캡처가 근거).
# 브로드캐스트·멀티캐스트는 보낸 레인에서 양쪽으로 뻗고, 지나가는 레인에는 받은 점을 찍는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in str(s)) else MONO
def tw(s, size):
    """글자 폭 추정 — 전각 1em, 라틴 0.62em."""
    return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(s))

W = 940
LANE_W, LANE_H, Y0 = 200, 44, 104
LX3 = (200, 480, 760)          # 레인 셋의 중심. stride 280
ROW = 52                       # 메시지 행 간격


class LabSeq(D):
    def __init__(s, h, eyebrow, title, desc, lead, lanes, xs=LX3):
        """lanes: [(키, 이름, 프로그램, 캡처 여부)]"""
        super().__init__(W, h, eyebrow, title, desc, lead)
        s.LX, s.order = {}, []
        for (key, name, sub, cap), x in zip(lanes, xs):
            s.LX[key] = x; s.order.append(key)
            s.box(x - LANE_W / 2, Y0, LANE_W, LANE_H, PAPER2, INK if cap else RULE, 1.4 if cap else 1.0)
            s.t(x, Y0 + 19, name, 13, INK, kr(name), "middle", 600)
            s.t(x, Y0 + 36, sub, 12, MUTED, kr(sub))
            if cap: s.chip(x, Y0 + LANE_H + 20, "캡처 지점", INK, 11)
        s.top = Y0 + LANE_H + 40
        s._axis = False

    def _t(s, t, y):
        """시각 한 칸. 시각이 하나라도 찍힐 때만 축 이름을 단다(시각 없는 장에 이름만 뜨지 않게)."""
        if not s._axis:
            s.t(24, s.top - 4, "시각(초)", 12, SOFT, KR, "start"); s._axis = True
        s.t(24, y + 4, t, 12, MUTED, MONO, "start")

    def rails(s, ybot):
        for x in s.LX.values():
            s.line(x, s.top, x, ybot, RULE, 1.0, "3 6")

    def _seg(s, a, b, y, c, dash, mk, dots=True):
        x1, x2 = s.LX[a], s.LX[b]; d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 8 * d} {y} L {x2 - 10 * d} {y}", c, 1.6, m=mk, dash=dash)
        if not dots: return
        # 지나가는 레인에 받은 점
        lo, hi = sorted((x1, x2))
        for k in s.order:
            if lo < s.LX[k] < hi:
                s.o.append(f'<circle cx="{s.LX[k]}" cy="{y}" r="3.2" fill="{c}"/>')

    def msg(s, a, b, label, y, c=MUTED, sub=None, t=None, missing=False, mk=None):
        """a → b 한 방향. 라벨은 b 쪽 마지막 칸 가운데에 둔다(가운데 레인 위에 앉지 않게)."""
        dash = "5 4" if missing else None
        c = SOFT if missing else c
        mk = mk or {MUTED: "ar", INFO: "info", ACC: "acc", WARN: "warn", OK: "ok", BAD: "bad", SOFT: "soft"}[c]
        s._seg(a, b, y, c, dash, mk, dots=False)
        xb = s.LX[b]; ia, ib = s.order.index(a), s.order.index(b)
        prev = s.order[ib - 1] if ib > ia else s.order[ib + 1]
        mx = (s.LX[prev] + xb) / 2
        s.t(mx, y - 9, label, 13, c if c != SOFT else MUTED, kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, kr(sub))
        if t is not None: s._t(t, y)

    def bcast(s, a, label, y, c=INFO, sub=None, t=None, label_to=None):
        """a 에서 양쪽 끝 레인으로. 라벨은 label_to 쪽 칸에."""
        ends = [s.order[0], s.order[-1]]
        mk = {INFO: "info", ACC: "acc", WARN: "warn", MUTED: "ar"}[c]
        for e in ends:
            if e != a: s._seg(a, e, y, c, None, mk)
        tgt = label_to or (s.order[-1] if a != s.order[-1] else s.order[0])
        xb = s.LX[tgt]; ia, ib = s.order.index(a), s.order.index(tgt)
        prev = s.order[ib - 1] if ib > ia else s.order[ib + 1]
        mx = (s.LX[prev] + xb) / 2
        s.t(mx, y - 9, label, 13, c, kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, kr(sub))
        if t is not None: s._t(t, y)

    def note(s, a, txt, y, c=MUTED, focal=False, t=None):
        """레인 위에 앉는 상태 칩 — 선 밖의 사건(로그·시그널·침묵)."""
        x = s.LX[a]; w = tw(txt, 13) + 24
        if focal: s.tone(x - w / 2, y - 14, w, 28, ACC, 6, "1f", 1.4)
        else: s.o.append(f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="6" fill="{PAPER}" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, ACC if focal else c, kr(txt), "middle", 600)
        if t is not None: s._t(t, y)

    def divider(s, y, label):
        s.line(24, y, W - 48, y, RULE, 1.0, "4 3")
        s.t(W - 48, y - 8, label, 12, SOFT, kr(label), "end", 600)
