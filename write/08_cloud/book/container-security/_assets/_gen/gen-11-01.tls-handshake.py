# 타입 스펙: type-sequence — 클라이언트가 서버 인증서를 검증하고 대칭키를 합의하는 기본 핸드셰이크, 그 위에 서버가 요구할 때만 mTLS 가 클라이언트 인증서 단계를 더한다. 레인 둘, 메시지 7, OPT 프레임 1(=focal).
# 사실 출처: 노트 L148~L152(소켓 열기·서버 인증서 요청, 인증서가 서버 신원과 공개키를 전달, 신뢰하는 CA 서명 확인, 대칭키 합의), L168(mTLS 는 서버 쪽에서 설정), L232(client-auth: need)
# 순서 메모: 노트는 mTLS 단계의 위치를 정하지 않는다. 대칭키 합의 뒤·데이터 앞에 둔 것은 TLS 1.3 에서 인증서 교환이 암호화된 구간에서 일어나는 순서에 맞춘 것이다(L154 가 TLS 1.3 을 언급).
# Layout conventions: 레인 폭 212, 메시지 stride 56(y=192·248·304·368), OPT 프레임 y=412~616, 프레임 안 메시지 y=488·544. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, both=False):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m=mk, dash=dash)
        if both:
            # 양방향: 시작점 쪽에 반대로 향하는 짧은 선분을 얹어 머리를 하나 더 단다
            s.path(f"M {x1+26*dr} {y} L {x1+12*dr} {y}", c, 1.5, m=mk)
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


W, H = 960, 788
d = SeqKR(W, H, "SEQUENCE · 11-01 §4",
          "서버가 요구하면 mTLS 가 클라이언트 인증서 단계를 더합니다",
          "클라이언트가 소켓을 열어 서버 인증서를 받고 신뢰하는 CA 의 서명을 확인한 뒤 대칭키를 합의한다. 서버가 client-auth: need 를 걸면 서버도 클라이언트 인증서를 받아 같은 확인을 한다.",
          lead="기본 핸드셰이크는 서버만 증명하고, mTLS 는 클라이언트의 증명을 더합니다")

LX = d.lanes([("클라이언트", "연결을 시작"), ("서버", "인증서를 보냄")], y0=104, lane_w=212)
d.rails(704)

d.msg("클라이언트", "서버", "연결 요청", 192, MUTED, sub="소켓 열기 · 서버 인증서 요청")
d.msg("서버", "클라이언트", "서버 인증서", 248, MUTED, mk="ar", dash="5 4", sub="서버 신원 · 공개키")
d.selfmsg("클라이언트", "CA 서명 확인", 304, OK, sub="신뢰하는 CA 가 서명했나")
d.msg("클라이언트", "서버", "대칭키 합의", 368, INFO, sub="이 연결의 나머지 메시지용", both=True)

# focal: 서버가 요구할 때만 더해지는 mTLS 단계
FX0, FX1, FY0, FY1 = 24, W - 24, 412, 624
d.box(FX0, FY0, FX1 - FX0, FY1 - FY0, f"{ACC}0F", ACC, 1.4, 4)
d.box(FX0, FY0, 44, 20, PAPER, ACC, 1.2, 2)
d.t(FX0 + 22, FY0 + 15, "OPT", 12, ACC, MONO, "middle", 600)
d.t(FX0 + 124, FY0 + 15, "[mTLS · client-auth: need]", 12, ACC, MONO, "start")
d.msg("서버", "클라이언트", "클라이언트 인증서 요청", 488, ACC, dash="5 4")
d.msg("클라이언트", "서버", "클라이언트 인증서", 544, ACC, sub="클라이언트 신원 · 공개키")
d.state("서버", "CA 서명 확인", 596, OK)

d.msg("클라이언트", "서버", "암호화된 메시지", 668, INFO, sub="합의한 대칭키 사용", both=True)

d.legend(724, [("CA 서명 확인", OK), ("대칭키", INFO), ("mTLS 가 더하는 단계", ACC), ("기본 핸드셰이크", MUTED)])
d.save(str(ASSETS / "11-01.tls-handshake.svg"))
print("ok 11-01 tls-handshake")
