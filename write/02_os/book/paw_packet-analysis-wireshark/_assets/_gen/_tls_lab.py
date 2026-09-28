# 04-04 실습 편 — 도식 공용 틀. 시퀀스(클라이언트·서버 두 레인)와 판단 흐름(타원·사각형·마름모)의 좌표를 한 벌로 고정한다.
# 같은 편의 도식이 stride 를 공유하도록 폭 880, 레인 폭 240, 메시지 간격 64 를 여기서만 정한다.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W = 880
EYEBROW = "PACKET ANALYSIS WITH WIRESHARK · 04-04 "

def kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def text_w(t, size):
    # 전각 1글자 = 1em, 라틴 = 0.62em (스타일 계약의 폭 예산)
    return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(t))

class SeqKR(Seq):
    """Seq 의 MONO 하드코딩을 한글 감지로 바꾼 서브클래스 (계약 §프리미티브가 한글을 mono 로 내보내는 자리)."""
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, kr(sub))
    def state(s, a, txt, y, c):
        x = s.LX[a]; w = text_w(txt, 11) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, kr(txt))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12, c, kr(label), "start", 600)
        if sub: s.t(x + 68, y + 14, sub, 11, MUTED, kr(sub), "start")
    def ghost(s, cx, y, txt, c=ACC):
        """오지 않은 메시지 자리 — 점선 칩."""
        w = text_w(txt, 11) + 24
        s.o.append(f'<rect x="{cx - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}12" stroke="{c}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        s.t(cx, y + 4, txt, 11, c, kr(txt), "middle", 600)
    def frame(s, x, y, w, h, op, guard=None):
        """결합 조각(alt·loop) 틀 — 참여 레인만 감싼다."""
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
        s.o.append(f'<rect x="{x}" y="{y}" width="48" height="18" rx="2" fill="{PAPER}" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
        s.t(x + 24, y + 13, op, 9, MUTED, MONO)
        if guard: s.t(x + 60, y + 14, guard, 12, MUTED, kr(guard), "start")
    def divider(s, x, y, w, guard=None):
        s.line(x + 8, y, x + w - 8, y, "rgba(245,245,245,0.20)", 1, "4 3")
        if guard: s.t(x + 60, y + 20, guard, 12, MUTED, kr(guard), "start")

def seq(tag, title, desc, lead, h):
    d = SeqKR(W, h, EYEBROW + tag, title, desc, lead)
    d.lanes([("클라이언트", "tls-client"), ("서버", "tls-server · 4433")], y0=104, lane_w=240)
    return d

class Flow(D):
    """판단 흐름 — 도형이 종류를 나른다 (타원=시작·끝, 사각형=조치, 마름모=판단)."""
    def oval(s, cx, y, w, h, txt, c=INK, focal=False):
        fill = ACC + "12" if focal else PAPER2
        s.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{ACC if focal else c}" stroke-width="{1.4 if focal else 1.1}"/>')
        s.t(cx, y + h / 2 + 5, txt, 13, ACC if focal else c, kr(txt), "middle", 600)
    def step(s, cx, y, w, h, title, sub, c=None):
        if c: s.tone(cx - w / 2, y, w, h, c, 6)
        else: s.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
        s.t(cx, y + 26, title, 13, c if c else INK, kr(title), "middle", 600)
        s.t(cx, y + 48, sub, 12, MUTED, kr(sub))
    def diamond(s, cx, y, hw, hh, txt, focal=False):
        cy, c = y + hh, (ACC if focal else INK)
        s.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
        s.t(cx, cy + 5, txt, 13, c, kr(txt), "middle", 600)
