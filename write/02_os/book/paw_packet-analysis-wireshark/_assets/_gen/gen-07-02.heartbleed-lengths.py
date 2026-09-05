# 07-02 §1 — Heartbleed 는 두 레코드의 길이 필드만 비교해도 드러난다. 원문 예제 프레임 15·16 의 실제 값.
# 타입 스펙: type-sequence — 두 참여자 사이의 요청·응답 왕복. 각 메시지에 레코드 길이를 달아
#           응답이 요청보다 긴 자리를 그대로 보이게 한다.
import sys; sys.path.insert(0, ".")
from dd import Seq, D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 960, 512
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-02 §1",
          "응답이 요청보다 32바이트 길다",
          "원문 heartbleed.pcap 의 프레임 15 와 16. 두 프레임 모두 레코드 타입 24 인 암호화된 Heartbeat 이고, 열어 볼 수 있는 것은 레코드 길이 하나뿐이다. 그 하나가 유출을 고발한다.",
          "암호화되어 있어도 길이 필드는 평문으로 남습니다")

d.lanes([("클라이언트 · 요청하는 쪽", "52.1.90.117:49578"),
         ("서버 · 취약한 OpenSSL", "10.0.0.3:443")], y0=104, lane_w=300)
d.rails(372)

d.msg("클라이언트 · 요청하는 쪽", "서버 · 취약한 OpenSSL",
      "Heartbeat Request", 206, MUTED,
      sub="tls.record.length == 112 · 프레임 183바이트")
d.state("서버 · 취약한 OpenSSL", "payload_length 를 안 봄", 258, BAD)
d.msg("서버 · 취약한 OpenSSL", "클라이언트 · 요청하는 쪽",
      "Heartbeat Response", 310, BAD, mk="bad",
      sub="tls.record.length == 144 · 프레임 215바이트")

d.tone(24, 386, 420, 44, ACC, 6)
d.t(36, 404, "144 − 112 = 32", 12, ACC, MONO, "start", 600)
d.t(36, 421, "요청하지 않은 32바이트가 딸려 나왔습니다", 11, MUTED, KR, "start")

d.box(468, 386, 468, 44, PAPER2, RULE, 1.0, 6)
d.t(480, 404, "5 + 112 = 117 · 5 + 144 = 149", 12, INK, MONO, "start", 600)
d.t(480, 421, "레코드 헤더 5바이트를 더하면 TCP 길이와 맞습니다", 11, MUTED, KR, "start")

d.legend(H - 60, [("유출이 실린 응답", BAD), ("길이 차이", ACC)])
d.save("07-02.heartbleed-lengths.svg")
