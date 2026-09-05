# 05-01 §2 — DHCPv6 의 네 메시지 교환(SARR). 원문 DHCPv6-Flow-SOLICIT.pcap 의 실제 주소·옵션·
# 트랜잭션 ID 만 쓴다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. headline(accent)은 주소가 확정되는
#           REPLY 하나. 프리미티브의 Seq.msg 가 한글을 MONO 로 하드코딩하므로 계약대로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 16, sub, 11, MUTED, KR)

W, H = 940, 584
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §2",
          "SARR — 네 메시지로 주소를 받습니다",
          "DHCPv6 의 네 메시지 교환. 클라이언트는 서버 주소를 모르므로 멀티캐스트로 보내고, 트랜잭션 ID 가 요청과 응답을 짝짓는다.",
          "앞 두 메시지와 뒤 두 메시지의 트랜잭션 ID 가 다릅니다 — 새 요청이기 때문입니다")

d.lanes([("클라이언트", "UDP 546"), ("서버", "UDP 547")], y0=104, lane_w=300)
d.rails(456)

d.msg("클라이언트", "서버", "SOLICIT", 200, INFO, "info",
      sub="msgtype==1 · 목적지는 멀티캐스트 ff02::1:2 · xid 0x10eafe")
d.msg("서버", "클라이언트", "ADVERTISE", 264, INFO, "info",
      sub="msgtype==2 · 서버 식별자(DUID) · 이름 서버 옵션 23")
d.msg("클라이언트", "서버", "REQUEST", 328, MUTED, "ar",
      sub="msgtype==3 · 새 xid 0x3ec03e · 고른 서버의 식별자를 담습니다")
d.msg("서버", "클라이언트", "REPLY", 392, ACC, "acc",
      sub="msgtype==7 · 같은 xid 0x3ec03e · 바인딩을 기록하고 주소를 확정합니다")

d.state("클라이언트", "IPv6 주소 확보", 432, OK)
d.selfmsg("클라이언트", "rapid commit 옵션", 480, WARN,
          sub="SOLICIT 에 넣으면 두 메시지로 줄어듭니다")

d.legend(H - 56, [("주소가 확정되는 지점", ACC), ("서버를 찾는 구간", INFO), ("두 메시지로 줄이는 옵션", WARN)])
d.save("05-01.sarr.svg")
