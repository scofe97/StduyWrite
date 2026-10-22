# 타입 스펙: type-sequence — 공개키로 잠그면 개인키로 풀고, 개인키로 서명하면 공개키로 검증한다: 같은 키 쌍을 반대 방향으로 쓴다. 레인 둘(소유자·상대), 메시지 방향이 논지.
# 사실 출처: 노트 L75~L82(공개키는 공유·개인키는 비공개, 개인키가 먼저 생성되고 공개키를 계산, 암호화와 서명의 방향이 반대)
# Layout conventions: 레인 폭 212, 메시지 stride 56(y=244·332·496), 프레임 두 개(암호화·서명) 높이 108, 상태 칩은 레인 중심. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    """계약 §프리미티브가 한글을 mono 로 내보내는 자리를 한글 스택·13/12px 로 바꾼다."""
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12, MUTED, kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 72, y - 4, label, 13, c, kr(label), "start", 600)
        if sub: s.t(x + 72, y + 14, sub, 12, MUTED, kr(sub), "start")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(12 if "가" <= ch <= "힣" else 7.4 for ch in txt) + 24
        s.o.append(f'<rect x="{x-w/2}" y="{y-12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x-w/2}" y="{y-12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, kr(txt))


W, H = 960, 636
d = SeqKR(W, H, "SEQUENCE · 11-01 §2",
          "공개키로 잠그면 개인키로 풀고, 개인키로 서명하면 공개키로 검증합니다",
          "개인키 소유자가 키 쌍을 만들어 공개키를 건네면, 암호문은 상대에서 소유자로, 서명은 소유자에서 상대로 흐른다. 같은 키 쌍을 반대 방향으로 쓴다.",
          lead="암호화와 서명은 같은 키 쌍을 반대 방향으로 씁니다")

LX = d.lanes([("소유자", "개인키 보유"), ("상대", "공개키 보유")], y0=104, lane_w=212)
d.rails(572)

# 준비: 개인키가 먼저 생기고 공개키는 거기서 계산한다
d.selfmsg("소유자", "개인키 생성 → 공개키 계산", 192, MUTED, sub="개인키가 먼저, 공개키는 거기서 유도")
d.msg("소유자", "상대", "공개키", 248, MUTED, sub="누구와도 공유 가능")

FX0, FX1 = 24, W - 24


def frame(y0, y1, tab, tw):
    d.box(FX0, y0, FX1 - FX0, y1 - y0, "rgba(245,245,245,0.04)", "rgba(245,245,245,0.22)", 1, 4)
    d.box(FX0, y0, tw, 20, PAPER, "rgba(245,245,245,0.22)", 1, 2)
    d.t(FX0 + tw / 2, y0 + 15, tab, 12, MUTED, KR, "middle", 600)


# 암호화: 공개키로 잠그고 개인키로 푼다 (상대 → 소유자)
frame(292, 400, "암호화 · 기밀성", 124)
d.msg("상대", "소유자", "암호문", 340, INFO, sub="공개키로 암호화")
d.state("소유자", "개인키로만 복호화", 384, INFO)

# 두 흐름의 방향이 반대라는 점이 이 그림의 논점
d.chip(W / 2, 428, "방향이 반대", ACC, 13, 8)

# 서명: 개인키로 서명하고 공개키로 검증한다 (소유자 → 상대)
frame(456, 564, "서명 · 신원 확인", 132)
d.msg("소유자", "상대", "서명", 504, OK, sub="개인키로 서명")
d.state("상대", "공개키로 검증 · 누구나", 548, OK)

d.legend(580, [("공유", MUTED), ("암호화", INFO), ("서명", OK), ("방향이 반대", ACC)])
d.save(str(ASSETS / "11-01.keypair-two-uses.svg"))
print("ok 11-01 keypair-two-uses")
