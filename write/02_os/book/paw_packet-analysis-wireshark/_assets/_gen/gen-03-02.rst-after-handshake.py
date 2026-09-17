# 03-02 §1 「드문 쪽」 — 원문 RST-01.pcap. handshake 두 번이 오간 뒤 ACK 가 와야 할 자리에 RST 가 온다.
# 아래 세 칸은 원문이 드는 설명 셋을 그대로 옮긴 것이고, 셋의 공통점이 결론 줄이다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 정상 흐름이라면 왔어야 할 ACK 를 흐린 점선으로
#           같은 자리에 겹쳐 두고, headline(bad)은 실제로 온 RST 하나다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 920, 604
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §1",
          "세 번째 자리에 RST 가 오면",
          "원문 RST-01.pcap 이다. SYN 과 SYN,ACK 가 오간 뒤 handshake 를 닫을 ACK 대신 RST 가 왔다. 원문이 드는 설명 셋은 모두 정상적인 소켓 API 사용으로는 나오지 않는 경로를 가리킨다.",
          "정상 소켓 API 로는 안 나오므로 애플리케이션보다 앞단을 먼저 봅니다")

d.lanes([("클라이언트", "122.167.84.137"), ("서버", "LISTEN 중")], y0=104, lane_w=280)
d.rails(352)

d.msg("클라이언트", "서버", "SYN", 196, INFO, "info")
d.msg("서버", "클라이언트", "SYN, ACK", 240, INFO, "info")
# 정상 흐름이라면 이 자리에 ACK 가 온다 — 흐린 점선으로 겹쳐 두고 바로 아래에 실제로 온 것을 그린다
d.msg("클라이언트", "서버", "ACK", 288, SOFT, "soft", dash="4,4", sub="정상 흐름이라면 여기")
d.msg("클라이언트", "서버", "RST", 344, BAD, "bad", sub="실제로 온 것 · 연결이 지워짐")

d.line(24, 388, W - 48, 388, RULE, 0.8, "4 6")
d.t(24, 414, "원문이 드는 설명 셋", 12, SOFT, KR, "start", 600)

BW, GAP = 264, 40
for i, (title, sub) in enumerate((("없던 연결", "RAW 패킷이 서버로"),
                                  ("클라이언트가 중단", "연결을 스스로 끊음"),
                                  ("번호가 어긋남", "시퀀스 변조 또는 위조"))):
    x = 24 + i * (BW + GAP)
    d.box(x, 428, BW, 68, PAPER2, RULE, 1.0, 8)
    d.t(x + BW / 2, 454, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, 474, sub, 11, MUTED, KR)

d.t(24, 522, "셋 다 앞단을 가리킴 — 로드밸런서 · 프록시 · 스캐너", 12, ACC, KR, "start", 600)

d.legend(H - 48, [("실제로 온 패킷", BAD), ("정상 흐름이라면", SOFT), ("정상 handshake", INFO)])
d.save("03-02.rst-after-handshake.svg")
