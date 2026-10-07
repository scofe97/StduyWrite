# 사실 출처: go doc net.Conn, PacketConn, Listener, TCPConn, UDPConn, UnixConn, IPConn (go1.25.1)
# 타입 스펙: type-uml-class
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560

d = D(W, H,
      "NET PACKAGE TYPE HIERARCHY",
      "net 패키지의 인터페이스와 구체 타입 계통",
      "Conn, PacketConn, Listener 인터페이스와 4대 구체 타입의 구현 관계",
      "스트림·패킷 추상 인터페이스와 OS 소켓을 감싸는 구체 타입 계통")

# defs 에 uml hollow triangle 마커 추가
d.o.insert(3, '<marker id="uml-realize" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><polygon points="1,1 9,5 1,9" fill="#0D1117" stroke="#8B98A9" stroke-width="1.2"/></marker>')
d.o.insert(4, '<marker id="uml-realize-acc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><polygon points="1,1 9,5 1,9" fill="#0D1117" stroke="#F08A59" stroke-width="1.2"/></marker>')

# ── 1. 인터페이스 행 (y = 96) ──
# net.Conn (focal interface)
d.box(48, 96, 264, 136, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(180, 110, "«interface»", 9, SOFT, fam=MONO, anchor="middle")
d.t(180, 126, "net.Conn", 13, ACC, fam=KR, anchor="middle", weight=600)
d.line(48, 134, 312, 134, RULE, 0.8)
d.t(60, 152, "+ Read(b)", 10, INK, fam=MONO, anchor="start")
d.t(60, 170, "+ Write(b)", 10, INK, fam=MONO, anchor="start")
d.t(60, 188, "+ Close()", 10, INK, fam=MONO, anchor="start")
d.t(60, 206, "+ LocalAddr() · RemoteAddr()", 10, INK, fam=MONO, anchor="start")
d.t(60, 224, "+ SetDeadline(t)", 10, INK, fam=MONO, anchor="start")

# net.PacketConn
d.box(352, 96, 272, 136, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(488, 110, "«interface»", 9, SOFT, fam=MONO, anchor="middle")
d.t(488, 126, "net.PacketConn", 13, INFO, fam=KR, anchor="middle", weight=600)
d.line(352, 134, 624, 134, RULE, 0.8)
d.t(364, 152, "+ ReadFrom(p)", 10, INK, fam=MONO, anchor="start")
d.t(364, 170, "+ WriteTo(p, addr)", 10, INK, fam=MONO, anchor="start")
d.t(364, 188, "+ Close()", 10, INK, fam=MONO, anchor="start")
d.t(364, 206, "+ LocalAddr()", 10, INK, fam=MONO, anchor="start")
d.t(364, 224, "+ SetDeadline(t)", 10, INK, fam=MONO, anchor="start")

# net.Listener
d.box(664, 96, 248, 112, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(788, 110, "«interface»", 9, SOFT, fam=MONO, anchor="middle")
d.t(788, 126, "net.Listener", 13, INK, fam=KR, anchor="middle", weight=600)
d.line(664, 134, 912, 134, RULE, 0.8)
d.t(676, 154, "+ Accept()", 10, INK, fam=MONO, anchor="start")
d.t(676, 174, "+ Close()", 10, INK, fam=MONO, anchor="start")
d.t(676, 194, "+ Addr()", 10, INK, fam=MONO, anchor="start")

# ── 2. 구체 타입 행 (y = 312) ──
# net.TCPConn
d.box(48, 312, 200, 136, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(148, 332, "net.TCPConn", 13, ACC, fam=KR, anchor="middle", weight=600)
d.line(48, 342, 248, 342, RULE, 0.8)
d.t(58, 360, "+ CloseRead()", 10, INK, fam=MONO, anchor="start")
d.t(58, 378, "+ CloseWrite()", 10, INK, fam=MONO, anchor="start")
d.t(58, 396, "+ SetKeepAlive()", 10, INK, fam=MONO, anchor="start")
d.t(58, 414, "+ SetLinger()", 10, INK, fam=MONO, anchor="start")
d.t(58, 432, "+ SetNoDelay()", 10, INK, fam=MONO, anchor="start")

# net.UDPConn
d.box(272, 312, 200, 136, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(372, 332, "net.UDPConn", 13, INFO, fam=KR, anchor="middle", weight=600)
d.line(272, 342, 472, 342, RULE, 0.8)
d.t(282, 360, "+ ReadFromUDP()", 10, INK, fam=MONO, anchor="start")
d.t(282, 378, "+ WriteToUDP()", 10, INK, fam=MONO, anchor="start")
d.t(282, 396, "+ ReadMsgUDP()", 10, INK, fam=MONO, anchor="start")
d.t(282, 414, "+ SetReadBuffer()", 10, INK, fam=MONO, anchor="start")
d.t(282, 432, "+ SetWriteBuffer()", 10, INK, fam=MONO, anchor="start")

# net.UnixConn
d.box(496, 312, 200, 136, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(596, 332, "net.UnixConn", 13, INK, fam=KR, anchor="middle", weight=600)
d.line(496, 342, 696, 342, RULE, 0.8)
d.t(506, 360, "+ CloseRead()", 10, INK, fam=MONO, anchor="start")
d.t(506, 378, "+ CloseWrite()", 10, INK, fam=MONO, anchor="start")
d.t(506, 396, "+ ReadFromUnix()", 10, INK, fam=MONO, anchor="start")
d.t(506, 414, "+ WriteToUnix()", 10, INK, fam=MONO, anchor="start")
d.t(506, 432, "+ ReadMsgUnix()", 10, INK, fam=MONO, anchor="start")

# net.IPConn
d.box(720, 312, 192, 136, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(816, 332, "net.IPConn", 13, INK, fam=KR, anchor="middle", weight=600)
d.line(720, 342, 912, 342, RULE, 0.8)
d.t(730, 360, "+ ReadFromIP()", 10, INK, fam=MONO, anchor="start")
d.t(730, 378, "+ WriteToIP()", 10, INK, fam=MONO, anchor="start")
d.t(730, 396, "+ ReadMsgIP()", 10, INK, fam=MONO, anchor="start")
d.t(730, 414, "+ SetReadBuffer()", 10, INK, fam=MONO, anchor="start")
d.t(730, 432, "+ SetWriteBuffer()", 10, INK, fam=MONO, anchor="start")

# ── 3. 관계선 (implements: dashed line + hollow triangle) ──
# TCPConn -> Conn (직선)
d.path("M 148 312 L 148 236", ACC, 1.2, m="uml-realize-acc", dash="5 4")

# UDPConn -> Conn (직교 ㄷ자)
d.path("M 330 312 L 330 272 L 240 272 L 240 236", MUTED, 1.0, m="uml-realize", dash="5 4")

# UDPConn -> PacketConn (직선)
d.path("M 410 312 L 410 236", INFO, 1.0, m="uml-realize", dash="5 4")

# UnixConn -> Conn (직교 ㄷ자)
d.path("M 540 312 L 540 284 L 280 284 L 280 236", MUTED, 1.0, m="uml-realize", dash="5 4")

# UnixConn -> PacketConn (직교 ㄷ자)
d.path("M 600 312 L 600 264 L 520 264 L 520 236", MUTED, 1.0, m="uml-realize", dash="5 4")

# IPConn -> PacketConn (직교 ㄷ자)
d.path("M 780 312 L 780 272 L 580 272 L 580 236", MUTED, 1.0, m="uml-realize", dash="5 4")

# 범례
d.legend(496, [
    ("인터페이스 구현 (implements)", MUTED),
    ("TCP 스트림 (focal)", ACC),
    ("패킷·데이터그램 지원", INFO)
])

d.save("01-01.interface-and-types.svg")
