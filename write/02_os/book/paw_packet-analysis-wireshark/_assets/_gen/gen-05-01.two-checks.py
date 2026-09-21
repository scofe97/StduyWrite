# 05-01 §5 — 주소 확인의 분담. 서버는 OFFER 전에 ICMP 로(끌 수 있음), 클라이언트는 ACK 뒤에 ARP 로 확인한다.
# 서버 장부에 없는 수동 설정 장비는 ARP 에서 잡히고, 클라이언트는 DECLINE 뒤 10초 이상 기다려 찾기부터 다시 한다.
# 근거는 RFC 2131 §3.1 2·5단계, RFC 826(요청은 브로드캐스트, 응답은 직접).
# 타입 스펙: type-sequence — 주체 셋(서버 · 클라이언트 · 수동 설정 장비) 사이의 시간순 메시지.
#           headline(accent)은 충돌을 드러내는 ARP 응답 하나. ICMP 확인은 서버 레인의 상태 칩으로 둔다.
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

W, H = 940, 740
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §5",
          "확인은 두 번, 두 장치가 나눠 한다",
          "서버는 OFFER 전에 ICMP 로 주소 X 를 확인하지만 이 확인은 끌 수 있다. 클라이언트는 ACK 뒤 ARP 요청을 브로드캐스트하고, 서버 장부에 없는 수동 설정 장비가 직접 응답하면 DECLINE 을 보낸 뒤 찾기부터 다시 한다.",
          "ACK 는 장부끼리의 충돌을, ARP 는 장부 밖의 사용자를 잡습니다")

d.lanes([("서버", "UDP 67"), ("클라이언트", "UDP 68"), ("수동 설정 장비", "주소 X 를 손으로 설정")], y0=104, lane_w=220)
d.rails(660)

d.msg("클라이언트", "서버", "DISCOVER", 200, INFO, "info", sub="브로드캐스트")
d.state("서버", "ICMP 로 X 확인 · 끌 수 있음", 244, SOFT)
d.msg("서버", "클라이언트", "OFFER", 292, INFO, "info", sub="yiaddr = X")
d.msg("클라이언트", "서버", "REQUEST", 348, MUTED, "ar", sub="옵션 50 = X")
d.msg("서버", "클라이언트", "ACK", 404, OK, "ok", sub="장부에 기록 · 장부끼리는 충돌 없음")
d.msg("클라이언트", "수동 설정 장비", "ARP 요청", 460, MUTED, "ar", sub="ff:ff:ff:ff:ff:ff · 누가 X 인가")
d.msg("수동 설정 장비", "클라이언트", "ARP 응답", 516, ACC, "acc", sub="직접 응답 · 내가 X")
d.msg("클라이언트", "서버", "DECLINE", 572, WARN, "warn", sub="X 는 이미 쓰임")
d.state("클라이언트", "10초 이상 뒤 DISCOVER 부터", 616, WARN)

d.legend(H - 56, [("충돌이 드러나는 자리", ACC), ("찾기 · 제안", INFO), ("장부의 확정", OK), ("되돌아가는 경로", WARN)])
d.save("05-01.two-checks.svg")
