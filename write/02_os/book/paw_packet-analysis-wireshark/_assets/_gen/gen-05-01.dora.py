# 05-01 §4 — DHCPv4 의 네 메시지 교환(DORA). 원문 DHCPv4.pcap 의 실제 필드값만 쓴다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. headline(accent)은 yiaddr 가
#           확정되는 ACK 하나. Seq.msg 의 MONO 하드코딩은 계약대로 서브클래스로 감싼다.
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

W, H = 940, 568
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §4",
          "DORA — IPv4 쪽의 네 메시지",
          "DHCPv4 의 네 메시지 교환. 클라이언트는 아직 주소가 없어 브로드캐스트로 보내고, yiaddr 필드가 0.0.0.0 에서 실제 주소로 채워지는 과정이 이 흐름의 뼈대다.",
          "yiaddr 필드 하나만 좇아도 어느 단계까지 갔는지가 보입니다")

d.lanes([("클라이언트", "UDP 68"), ("서버", "UDP 67")], y0=104, lane_w=300)
d.rails(456)

d.msg("클라이언트", "서버", "DISCOVER", 200, INFO, "info",
      sub="option.dhcp==1 · 255.255.255.255 브로드캐스트 · yiaddr 0.0.0.0")
d.msg("서버", "클라이언트", "OFFER", 264, INFO, "info",
      sub="option.dhcp==2 · yiaddr 10.0.0.106 · 옵션 54 서버 식별자")
d.msg("클라이언트", "서버", "REQUEST", 328, MUTED, "ar",
      sub="option.dhcp==3 · 다시 브로드캐스트 · 옵션 54 로 서버를 지목합니다")
d.msg("서버", "클라이언트", "ACK", 392, ACC, "acc",
      sub="option.dhcp==5 · yiaddr 10.0.0.106 확정 · 바인딩을 저장합니다")

d.state("클라이언트", "ARP 로 중복 확인", 432, OK)
d.selfmsg("클라이언트", "이미 쓰이는 주소면 DECLINE", 480, WARN,
          sub="설정 과정을 처음부터 다시 시작합니다")

d.legend(H - 52, [("주소가 확정되는 지점", ACC), ("주소를 찾는 구간", INFO), ("충돌 시 되돌아가는 경로", WARN)])
d.save("05-01.dora.svg")
