# 03-05 §4 — ECN 은 IP 헤더의 2비트와 TCP 헤더의 플래그 둘이 층을 나눠 맡는다. 라우터의 도장은 IP 에, 되돌림은 TCP 에 실린다.
# 노트의 읽기: 2026-09-08 회차에서 학습자가 ECN·ECT·CE·ECE·CWR 을 한 층으로 뭉쳐 막혀 추가한 도식.
#   RFC 3168 §5: "This uses an ECN field in the IP header with two bits, making four ECN codepoints, '00' to '11'."
#   RFC 3168 §5: "The CE codepoint '11' is set by a router to indicate congestion to the end nodes."
#   RFC 3168 §6.1: "ECN uses the ECT and CE flags in the IP header (as shown in Figure 1) for signaling between routers
#       and connection endpoints, and uses the ECN-Echo and CWR flags in the TCP header (as shown in Figure 4) for
#       TCP-endpoint to TCP-endpoint signaling."
#   RFC 3168 §6.1: "To enable the TCP receiver to determine when to stop setting the ECN-Echo flag, we introduce a second
#       new flag in the TCP header, the CWR flag."
#   RFC 3168 §6.1.1: "We call a SYN packet with the ECE and CWR flags set an "ECN-setup SYN packet" ... we call a SYN-ACK
#       packet with only the ECE flag set but the CWR flag not set an "ECN-setup SYN-ACK packet""
# 타입 스펙: type-sequence — 참여자 레인 + 시간축. 협상(TCP 플래그·연결마다 한 번)과 데이터(IP 코드·패킷마다)를
#       가로 구분선으로 갈랐고, 헤드라인(강조색)은 라우터가 ECT 를 CE 로 고쳐 써서 넘기는 한 화살표뿐이다.
#       축약: 핸드셰이크의 세 번째 ACK 와 SYN-ACK 의 IP 코드는 그리지 않는다. 라우터를 지나는 종단 간 메시지는
#       홉을 둘로 쪼개지 않고 한 화살표로 긋되 라벨을 라우터 생명선 밖으로 비켰다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, PAPER, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=0):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + lx
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12, MUTED, KR)
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 14, sub, 12, MUTED, KR, "start")
    def phase(s, y, txt):
        # 협상/데이터 구분선. UML 프래그먼트가 아니라 단계 표시라 프레임 대신 점선 + 칩으로 둔다.
        # 점선은 칩 폭만큼 비워 두 토막으로 긋는다 — 칩 뒤로 지나가면 글자가 선에 닿는다(dd-lint text-line).
        w = len(txt) * 11 + 14
        s.line(40, y, s.w / 2 - w / 2 - 8, y, RULE, 0.8, "4 4")
        s.line(s.w / 2 + w / 2 + 8, y, s.w - 40, y, RULE, 0.8, "4 4")
        s.chip(s.w / 2, y, txt, SOFT, 11)

W, H = 1000, 712
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §4",
          "ECN 은 두 층이 나눠 맡습니다",
          "라우터가 끼는 신호는 IP 헤더의 2비트(ECT→CE)이고 종단끼리 주고받는 신호는 TCP 플래그(ECE·CWR)다. "
          "협상은 종단끼리의 일이라 TCP 플래그로만 하고, 데이터가 흐를 때는 IP 의 도장과 TCP 의 되돌림이 이어진다.",
          "라우터의 도장은 IP 에, 되돌림은 TCP 에 실립니다")
d.lanes([("송신자", "TCP + IP"), ("라우터", "IP 헤더까지만 봅니다"), ("수신자", "TCP + IP")])
d.rails(580)

d.phase(172, "협상 · TCP 플래그 · 연결마다 한 번")
d.msg("송신자", "수신자", "SYN · ECE + CWR", 204, OK, sub="플래그 둘을 세움 — 「ECN 할 수 있다」", lx=-185)
d.msg("수신자", "송신자", "SYN-ACK · ECE", 248, OK, dash="5 4", sub="ECE 만 세움 — 「나도 할 수 있다」", lx=185)

d.phase(292, "데이터 · 라우터는 IP 코드 · 종단은 TCP 플래그")
d.msg("송신자", "라우터", "데이터 · IP: ECT(0)", 328, INFO, sub="「이 연결은 ECN 을 이해한다」")
d.selfmsg("라우터", "큐가 차기 시작", 372, MUTED, sub="버리는 대신 CE 로 고쳐 씀")
d.msg("라우터", "수신자", "데이터 · IP: CE", 416, ACC, mk="acc", sub="「여기 붐빈다」 — 라우터의 도장")
d.msg("수신자", "송신자", "ACK · TCP: ECE", 460, OK, dash="5 4", sub="「CE 를 봤다」 — 되돌림은 TCP 에", lx=185)
d.selfmsg("송신자", "cwnd 절반", 504, MUTED, sub="손실 때와 같은 반응")
d.msg("송신자", "수신자", "데이터 · TCP: CWR (IP: ECT)", 548, OK, sub="「줄였다」 — 수신자가 ECE 를 그침", lx=-185)

d.t(20, 612, "IP 헤더의 2비트는 네 상태입니다 — Not-ECT(00) · ECT(0)(10) · ECT(1)(01) · CE(11). 호스트는 ECT 를 쓰고 라우터는 CE 를 씁니다.",
    11, MUTED, KR, "start")
d.t(20, 634, "TCP 헤더의 플래그 둘(ECE·CWR)은 종단끼리 주고받습니다. 라우터가 끼는 표시는 IP 에 있습니다 — 라우터는 망 층까지만 구현합니다.",
    11, MUTED, KR, "start")
d.legend(H - 52, [("TCP 플래그 · 종단끼리", OK), ("IP: ECT · 호스트가 씀", INFO), ("IP: CE · 라우터가 씀", ACC)])
d.save("03-05.ecn-two-layers.svg")
print("ok 03-05.ecn-two-layers")
