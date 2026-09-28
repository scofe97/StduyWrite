# 05-04 실습 편 — 단계 하나의 캡처를 시퀀스로 그리는 공용 틀. 값은 전부 ~/study/paw-lab/05-dhcp/pcap/ 의 실제 프레임.
# 줄마다: 왼쪽 여백에 프레임 번호, 레인 사이에 메시지. 캡처한 자리는 레인 머리 아래 칩으로 표시한다.
# Seq 프리미티브가 한글을 mono 로 찍는 자리를 서브클래스로 감싼다(계약 §프리미티브가 한글을 mono 로 내보내는 자리).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W = 920          # 본문 삽입 폭 880~1000 의 하한 쪽
LANE_Y = 104     # 레인 머리 위치
STRIDE = 52      # 메시지 줄 간격 (서브 라벨 포함, 4의 배수)
TAB = 36         # 구획 머리(탭) 높이
TAG_X = 36       # 프레임 번호 칸

def kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class LabSeq(Seq):
    def __init__(s, h, eyebrow, title, desc, lead):
        super().__init__(W, h, eyebrow, title, desc, lead)
        s.y = 0

    def cast(s, names, lane_w=200, capture=None):
        """names: (이름, 부제). capture: 캡처를 돌린 레인 이름."""
        s.lanes(names, LANE_Y, lane_w)
        s.lane_w = lane_w
        if capture:
            s.cap(capture)
        s.y = LANE_Y + 44 + (44 if capture else 28)

    def lanes(s, names, y0=104, lane_w=210):
        """Seq.lanes 와 같되 부제의 글꼴을 한글 여부로 가른다."""
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def cap(s, lane):
        x = s.LX[lane]
        w = 120
        s.tone(x - w / 2, LANE_Y + 52, w, 20, INFO, 4, "22", 1.0)
        s.t(x, LANE_Y + 66, "캡처 · tcpdump", 12, INFO, KR)

    def region(s, label, n_msgs, extra=0):
        """메시지 n 줄을 감싸는 구획. 반환값은 구획 첫 메시지의 y."""
        top = s.y
        h = TAB + n_msgs * STRIDE + 8 + extra
        s.box(20, top, W - 64, h, "none", RULE, 1.0, 6)
        s.t(min(s.LX.values()) + 16, top + 24, label, 12, SOFT, kr(label), "start", 600)
        s.y = top + h + 16
        return top + TAB + 20

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, tag=None, lw=1.5):
        x1, x2 = s.LX[a], s.LX[b]; d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, lw, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, kr(sub))
        if tag: s.t(TAG_X, y + 4, tag, 12, SOFT, MONO, "start")

    def note(s, a, txt, y, c):
        """레인 위의 상태 칩 — 한글 폭 예산 1em."""
        x = s.LX[a]
        w = sum(13 if "가" <= ch <= "힣" else 8 for ch in txt) + 20
        s.tone(x - w / 2, y - 11, w, 22, c, 4, "22", 1.1)
        s.t(x, y + 4, txt, 12, c, kr(txt))

    def bracket(s, x, y1, y2, label, c, sub=None, ly=None):
        """레인 오른쪽의 세로 괄호 — 두 프레임 사이의 시간 구간."""
        s.path(f"M {x} {y1} L {x + 8} {y1} L {x + 8} {y2} L {x} {y2}", c, 1.4)
        my = ly if ly is not None else (y1 + y2) / 2
        s.t(x + 16, my + (0 if sub else 4), label, 12, c, kr(label), "start", 600)
        if sub: s.t(x + 16, my + 18, sub, 12, MUTED, kr(sub), "start")

    def finish(s, legend, fname):
        s.rails(s.y - 8)
        s.legend(s.h - 56, legend)
        s.save(fname)

def height(n_rows_total, n_regions, capture=True, extra=0):
    """캔버스 높이 — 레인 머리 + 구획들 + 범례."""
    return LANE_Y + 44 + (44 if capture else 28) + n_regions * (TAB + 8 + 16) + n_rows_total * STRIDE + extra + 80
