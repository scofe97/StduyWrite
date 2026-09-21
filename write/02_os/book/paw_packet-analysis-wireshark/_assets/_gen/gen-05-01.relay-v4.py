# 05-01 §5 — IPv4 릴레이. 클라이언트의 브로드캐스트는 라우터에서 멈추고, 라우터의 릴레이 에이전트가
# giaddr 에 자기 인터페이스 주소를 적어 설정된 서버 주소로 유니캐스트한다. 서버는 giaddr 로 응답한다.
# 근거는 RFC 2131 §1.5·§4.1, RFC 1542 §4.1.1.
# 타입 스펙: type-sequence — 주체 셋(클라이언트 · 릴레이 · 서버) 사이의 시간순 메시지.
#           headline(accent)은 브로드캐스트가 유니캐스트로 바뀌어 세그먼트를 넘는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
def _w(t, size): return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(t))
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, KR)
    def lanes(s, names, y0=104, lane_w=210):
        LX = Seq.lanes(s, [(nm, "") for nm, _ in names], y0, lane_w)
        for nm, sub in names:  # 서브라벨만 한글 스택으로 다시 찍는다
            s.t(LX[nm], y0 + 37, sub, 12, MUTED, _kr(sub))
        return LX
    def state(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 12) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')  # 레인 점선 가림
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))

W, H = 940, 572
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §5",
          "릴레이가 브로드캐스트를 대신 전달한다",
          "세그먼트 A 의 클라이언트가 보낸 DISCOVER 브로드캐스트는 라우터에서 멈춘다. 라우터의 릴레이 에이전트가 giaddr 에 자기 주소를 적어 세그먼트 B 의 서버로 유니캐스트하고, 서버는 giaddr 로 응답해 릴레이가 클라이언트에게 내려 준다.",
          "세그먼트를 넘는 구간이 유니캐스트로 바뀝니다 — 클라이언트 쪽에서는 릴레이가 없을 때와 같습니다")

d.lanes([("클라이언트", "세그먼트 A"), ("릴레이 에이전트", "라우터"), ("서버", "세그먼트 B")], y0=104, lane_w=220)
d.rails(492)

d.msg("클라이언트", "릴레이 에이전트", "DISCOVER", 200, INFO, "info", sub="255.255.255.255")
d.state("릴레이 에이전트", "giaddr ← 받은 인터페이스 주소", 244, SOFT)
d.msg("릴레이 에이전트", "서버", "DISCOVER", 292, ACC, "acc", sub="유니캐스트 · 설정된 서버 주소")
d.msg("서버", "릴레이 에이전트", "OFFER", 348, INFO, "info", sub="giaddr 로 응답")
d.msg("릴레이 에이전트", "클라이언트", "OFFER", 404, INFO, "info", sub="세그먼트 A 로 전달")
d.state("릴레이 에이전트", "REQUEST · ACK 도 같은 길", 452, SOFT)

d.legend(H - 56, [("세그먼트를 넘는 유니캐스트", ACC), ("세그먼트 안의 메시지", INFO)])
d.save("05-01.relay-v4.svg")
