# 08-01 §4 「기본 출력에 실리는 것」 — 질의 하나가 dnstap 메시지 넷이 되는 순서와, 기본·full 에서 각 메시지에 실리는 것.
# 소스 근거: plugin/dnstap/handler.go — SetQueryAddress(주소·포트·프로토콜), SetQueryTime, Message_CLIENT_QUERY,
#            IncludeRawMessage 일 때만 QueryMessage(원문). setup.go:130 `IncludeRawMessage = ... args[1] == "full"`.
#            FORWARDER_* 는 forward 플러그인이 낸다(본문 노트의 읽기).
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 왕복이고, 메시지마다 붙는 유형 이름이 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO, INFO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 38, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar"):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk)
        s.t((x1 + x2) / 2, y - 10, label, 13, c, _kr(label), "middle", 600)


W, H = 880, 640
d = SeqKR(W, H, "LEARNING COREDNS · 08-01 §4",
          "질의 하나가 dnstap 메시지 넷이 된다",
          "CoreDNS 는 클라이언트 질의를 받을 때, 상류에 전달할 때, 상류 응답을 받을 때, 클라이언트에 답할 때 메시지를 하나씩 남긴다. "
          "기본으로는 시각과 주소·포트·프로토콜만 실리고, full 을 붙여야 DNS 메시지 원문이 실린다.",
          "주황 칸이 full 이 더하는 것입니다")

d.lanes([("클라이언트", "stub resolver"), ("CoreDNS", "dnstap · forward"), ("상류 서버", "8.8.8.8")],
        y0=104, lane_w=230)
d.rails(436)


def chip(a, txt, y):
    x = d.LX[a]
    w = len(txt) * 7.4 + 22
    for f, st, sw in ((PAPER, "none", 0), (INFO + "22", INFO, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 5, txt, 12, INFO, MONO)


d.msg("클라이언트", "CoreDNS", "질의", 196)
chip("CoreDNS", "CLIENT_QUERY", 222)
d.msg("CoreDNS", "상류 서버", "전달", 270)
chip("CoreDNS", "FORWARDER_QUERY", 296)
d.msg("상류 서버", "CoreDNS", "응답", 344)
chip("CoreDNS", "FORWARDER_RESPONSE", 370)
d.msg("CoreDNS", "클라이언트", "응답", 418)
chip("CoreDNS", "CLIENT_RESPONSE", 444)

d.box(20, 474, 410, 70, PAPER2, RULE, 1.0, 6)
d.t(36, 500, "기본 · 메시지마다", 13, INK, KR, "start", 600)
d.t(36, 524, "시각 · 주소 · 포트 · 프로토콜", 12, MUTED, KR, "start")
d.tone(450, 474, 410, 70, ACC, 6, "12", 1.4)
d.t(466, 500, "full · 여기에 더해", 13, ACC, KR, "start", 600)
d.t(466, 524, "DNS 메시지 원문 · 와이어 형식", 12, MUTED, KR, "start")

d.t(20, 572, "FORWARDER_* 두 줄은 forward 플러그인이 있을 때만", 13, MUTED, KR, "start")

d.legend(590, [("메시지 유형", INFO), ("full 이 더하는 것", ACC)])
d.save("08-01.dnstap-seq.svg")
