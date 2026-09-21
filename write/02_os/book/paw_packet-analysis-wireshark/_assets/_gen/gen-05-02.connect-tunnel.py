# 05-02 §4 — 프록시를 거친 HTTPS. 클라이언트가 프록시에게 평문 CONNECT 로 목적지를 알리고, 200 을 받은 뒤로
# 프록시는 바이트를 그대로 넘긴다. 그 터널 안으로 4장의 TLS 1.2 핸드셰이크가 그대로 지나가므로 ClientHello 와
# SNI 는 평문이고, 내용이 안 보이기 시작하는 곳은 ChangeCipherSpec 다음이다.
# 본문 요구: 노트의 "그 뒤부터는 터널이라 내용이 안 보입니다" 가 터널이 암호화한다고 읽혔다(후보 19).
#            안 보이는 이유는 TLS 이고, CONNECT 는 프록시에게 · SNI 는 서버에게 하는 말임을 보인다.
# 근거: RFC 9110 §3.7(tunnel = blind relay) · §9.3.6(CONNECT host:port, 2xx 뒤 tunnel mode).
#       순서와 라벨은 2026-09-21 tshark 4.6.8 실측 — curl --tls-max 1.2 -x http://127.0.0.1:3128
#       https://example.com/ 을 클라이언트 ↔ 프록시 구간(lo0)에서 잡았다.
# 타입 스펙: type-sequence — 주체 셋(클라이언트 · 프록시 · 서버) 사이의 시간순 메시지.
#           focal 은 터널 안을 평문으로 지나가는 ClientHello 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
def _w(t, size): return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(t))
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, KR)
    def lanes(s, names, y0=104, lane_w=210):
        LX = Seq.lanes(s, [(nm, "") for nm, _ in names], y0, lane_w)
        for nm, sub in names:
            s.t(LX[nm], y0 + 37, sub, 12, MUTED, _kr(sub))
        return LX
    def state(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 12) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))

W, H = 940, 720
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §4",
          "CONNECT 뒤를 가리는 것은 터널이 아니라 TLS",
          "클라이언트가 프록시에게 CONNECT example.com:443 을 평문으로 보내고 200 을 받는다. 그 뒤로 프록시는 받은 바이트를 바꾸지 않고 넘기기만 하고, 그 안으로 TLS 1.2 핸드셰이크가 지나간다. ClientHello 와 SNI, ServerHello 와 인증서는 평문이고 ChangeCipherSpec 다음부터 암호화된다.",
          "CONNECT 는 프록시에게, SNI 는 서버에게 하는 말입니다 — 캡처는 클라이언트와 프록시 사이에서 떴습니다")

LX = d.lanes([("클라이언트", "curl"), ("프록시", "127.0.0.1:3128"), ("서버", "example.com:443")], y0=104, lane_w=200)
CL, PX = LX["클라이언트"], LX["프록시"]
LEFT_MID = (CL + PX) / 2            # 캡처 구간의 가운데 — 터널을 지나는 메시지의 라벨 자리

# 캡처한 구간 — 클라이언트와 프록시 사이
ZY0, ZY1 = 164, 652
d.o.append(f'<rect x="{CL + 20}" y="{ZY0}" width="{PX - CL - 48}" height="{ZY1 - ZY0}" rx="6" '
           f'fill="rgba(245,245,245,0.03)" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(CL + 28, ZY0 + 18, "캡처한 구간", 12, SOFT, KR, "start", 600)
d.rails(ZY1)

Y = [212, 264, 316, 360, 412, 464, 516, 568, 620]
d.msg("클라이언트", "프록시", "CONNECT example.com:443", Y[0], INFO, "info", sub="평문 · 프록시에게 목적지")
d.msg("프록시", "서버", "TCP 연결", Y[1], MUTED, "ar", sub="SYN · SYN/ACK · ACK")
d.msg("프록시", "클라이언트", "200 Connection established", Y[2], INFO, "info", dash="5 4", sub="평문 · 여기부터 터널")
# 프록시가 하는 일 — 캡처 구간과 겹치지 않게 프록시 레인 오른쪽에 붙인다
TXT = "터널 · 바이트를 그대로 넘김"
CW_ = _w(TXT, 12) + 20
d.o.append(f'<rect x="{PX + 16}" y="{Y[3] - 12}" width="{CW_}" height="24" rx="4" fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')
d.t(PX + 16 + CW_ / 2, Y[3] + 5, TXT, 12, MUTED, KR)
d.msg("클라이언트", "서버", "ClientHello", Y[4], ACC, "acc", sub="평문 · SNI=example.com", lx=LEFT_MID)
d.msg("서버", "클라이언트", "ServerHello · Certificate", Y[5], INFO, "info", dash="5 4", sub="평문 · TLS 1.2", lx=LEFT_MID)
d.msg("클라이언트", "서버", "ClientKeyExchange · CCS", Y[6], INFO, "info", sub="CCS 는 평문 · 다음 Finished 부터 보호", lx=LEFT_MID)
d.msg("서버", "클라이언트", "CCS · Finished", Y[7], WARN, "warn", dash="5 4", sub="Finished 부터 암호화", lx=LEFT_MID)
d.msg("클라이언트", "서버", "Application Data", Y[8], WARN, "warn", sub="요청과 응답 · 키 없이 못 읽음", lx=LEFT_MID)

d.legend(H - 56, [("터널 안의 평문 ClientHello", ACC), ("평문", INFO), ("암호화", WARN)])
d.save("05-02.connect-tunnel.svg")
